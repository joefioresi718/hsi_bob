import pandas as pd
import numpy as np


# Create master dict, add to it later.
master_df = pd.DataFrame()

# Use poverty file for zip codes.
acs_pov_file = pd.read_csv('clean_data/ACS 2020 Table 10 HH Poverty.csv')

# Get zip code list.
# Get rid of zip codes with 0 households.
acs_pov_file = acs_pov_file[acs_pov_file['Poverty status in the past 12 months by household type by age of householder, households, total'] != 0]
zcta_list = acs_pov_file['Zip code tablulation area (ZCTA)'].tolist()

# Get poverty ratios to add.
poverty_ratios = {zip_code: float(y / x) for zip_code, x, y in zip(zcta_list, acs_pov_file[
    'Poverty status in the past 12 months by household type by age of householder, households, total'].tolist(), acs_pov_file[
    'Poverty status in the past 12 months by household type by age of householder, households, total, income in the past 12 months below poverty level'
    ].tolist())}


# Add cdc file data.
# cdc_dict = pd.read_excel('data/CDC Places Data Dictionary.xlsx')
cdc_file = pd.read_csv('data/CDC Places 2020 Health Outcomes.csv')

# Rename zcta5 to zcta.
cdc_file['zcta']  = cdc_file['zcta5']
cdc_file.drop(columns=['zcta5'], inplace=True)
# Move zcta to front (for looks).
cols = cdc_file.columns.tolist()
cols = [cols[-1]] + cols[:-1]
cdc_file = cdc_file[cols]
# Sort by zip codes.
cdc_file.sort_values(by=['zcta'], inplace=True, ascending=True, ignore_index=True)
# Drop duplicates.
cdc_file = cdc_file.drop_duplicates()

# Selecting only relevant zip codes.
cdc_file['zcta'] = pd.Categorical(cdc_file['zcta'], categories=zcta_list, ordered=True)
cdc_file = cdc_file[cdc_file['zcta'].isin(zcta_list)]
# Drop NaN mental health stats.
cdc_file.dropna(subset=['mhlth_crudeprev'], inplace=True)

# Add CDC data to master dict.
master_df = pd.concat([master_df, cdc_file], ignore_index=True)
# print(master_df.head(10))

# Add hospital data.
hospital_file = pd.read_csv('data/Hospital Compare 2020.csv')

# Only use zip codes in master file.
hospital_file['zip_code'] = pd.Categorical(hospital_file['zip_code'], categories=master_df['zcta'].tolist(), ordered=True)
hospital_file = hospital_file[hospital_file['zip_code'].isin(zcta_list)]

# Drop 'irrelevant' categories.
hospital_file.drop(columns=['year', 'hospital_compare_id', 'address', 'city', 'state', 'county_name', 'phone_number', 'hospital_type', 'hospital_ownership', 'emergency_services', 'meets_criteria_for_meaningful_use_of_ehrs', 'hospital_overall_rating_footnote', 'mortality_national_comparison_footnote', 'safety_of_care_national_comparison_footnote', 'readmission_national_comparison_footnote', 'patient_experience_national_comparison_footnote', 'effectiveness_of_care_national_comparison_footnote', 'timeliness_of_care_national_comparison_footnote', 'efficient_use_of_medical_imaging_national_comparison_footnote'], inplace=True)

# Deal with hospital duplicates within zip codes.
hospital_duplicates = hospital_file[hospital_file.duplicated(subset=['zip_code'], keep=False)]
hospital_duplicates.sort_values(by=['zip_code'], inplace=True, ascending=True, ignore_index=True)

duplicated_zip_codes = list(set(hospital_duplicates['zip_code'].tolist()))

hospital_agg_stats = {}
for zip_code in duplicated_zip_codes:
    hospital_agg_stats[zip_code] = {}
    dup_series = hospital_duplicates[hospital_duplicates['zip_code'] == zip_code]
    for row in dup_series:
        for col in dup_series.columns:
            if str(col) != 'zip_code':
                if col not in hospital_agg_stats:
                    hospital_agg_stats[zip_code][col] = []
                hospital_agg_stats[zip_code][col].append(dup_series[col])

print(hospital_agg_stats)

print(len(hospital_file), len(set(hospital_file['zip_code'].tolist())))

exit()

# master_df_dict
# for col in cdc_cols:
#     col_data = [cdc_file[cdc_file['zcta5'] == zcta][col] for zcta in zcta_list]
#     col_data = [x.tolist()[0] if len(x) == 1 else None for x in col_data]
#     master_df_dict[col] = col_data


# mhlth_crudeprev = [cdc_file[cdc_file['zcta5'] == zcta]['mhlth_crudeprev'] for zcta in zcta_list]
# mhlth_crudeprev = [x.tolist()[0] if len(x) == 1 else None for x in mhlth_crudeprev]
# print([len(x) for x in mhlth_crudeprev])
# mhlth_crudeprev = [x[0] for x in mhlth_crudeprev if len(x) == 1]
# print(mhlth_crudeprev[150])
# num_households = acs_pov_file['Poverty status in the past 12 months by household type by age of householder, households, total'].tolist()

# num_population = [cdc_file[cdc_file['zcta5'] == zcta]['totalpopulation'] for zcta in zcta_list]
# num_population = [x.tolist()[0] if len(x) == 1 else 0 for x in num_population]
# pop_array = np.array(num_population)
# mean_pop = pop_array.mean()
# print(f'Mean population across zip codes: {mean_pop:.2f}')


master_df = pd.DataFrame(master_df_dict)
# No PR :(
master_df = master_df[master_df['zcta'] >= 1000]
# master_df = master_df[master_df['poverty_ratio'] == 1.0]
# master_df = master_df[master_df['num_households'] > mean_pop]
# print(len(master_df))
# print(master_df.head(10))

master_df['norm_pop'] = (master_df['total_population'] - master_df['total_population'].min()) / (master_df['total_population'].max() - master_df['total_population'].min())
master_df['norm_crude_mhlth'] = (master_df['crude_mhlth'] - master_df['crude_mhlth'].min()) / (master_df['crude_mhlth'].max() - master_df['crude_mhlth'].min())
master_df['norm_poverty_ratio'] = (master_df['poverty_ratio'] - master_df['poverty_ratio'].min()) / (master_df['poverty_ratio'].max() - master_df['poverty_ratio'].min())

master_df['weighted_score'] = master_df['norm_pop']**0.33 + master_df['norm_crude_mhlth']**0.33 + master_df['norm_poverty_ratio']**0.33
master_df['weighted_score'] = (master_df['weighted_score'] - master_df['weighted_score'].min()) / (master_df['weighted_score'].max() - master_df['weighted_score'].min())
master_df.sort_values(by=['weighted_score'], inplace=True, ascending=False, ignore_index=True)
print(master_df.head(10))


