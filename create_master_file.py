import pandas as pd
import numpy as np


# Create master dict, add to it later.
master_df = pd.DataFrame()

# Use poverty file for zip codes.
pov_file = pd.read_csv('clean_data/ACS 2020 Table 10 HH Poverty.csv')
pov_file = pd.read_csv('clean_data/ACS 2020 Table 10 HH Poverty.csv')

# Get zip code list.
# Get rid of zip codes with 0 households.
pov_file = pov_file[pov_file['Poverty status in the past 12 months by household type by age of householder, households, total'] != 0]
zcta_list = pov_file['Zip code tablulation area (ZCTA)'].tolist()
pov_file = pov_file[pov_file['Poverty status in the past 12 months by household type by age of householder, households, total'] != 0]
zcta_list = pov_file['Zip code tablulation area (ZCTA)'].tolist()

# Add cdc file data.
# cdc_dict = pd.read_excel('data/CDC Places Data Dictionary.xlsx')
cdc_file = pd.read_csv('data/CDC Places 2020 Health Outcomes.csv')

# Rename zcta5 to zcta.
cdc_file.rename(columns={'zcta5': 'zcta'}, inplace=True)

# Sort by zip codes.
cdc_file.sort_values(by=['zcta'], inplace=True, ascending=True, ignore_index=True)
# Drop duplicates.
cdc_file = cdc_file.drop_duplicates()

# Selecting only relevant zip codes.
cdc_file['zcta'] = pd.Categorical(cdc_file['zcta'], categories=zcta_list, ordered=True)
cdc_file = cdc_file[cdc_file['zcta'].isin(zcta_list)]
# Drop NaN mental health stats.
cdc_file.dropna(subset=['mhlth_crudeprev'], inplace=True)

# Normalize all cdc data.
def minmax_normalize(series):
    min_val = series.min()
    max_val = series.max()
    return (series - min_val) / (max_val - min_val)

cdc_cols = cdc_file.columns[1:]
for col in cdc_cols:
    cdc_file[col] = minmax_normalize(cdc_file[col])

# Add CDC data to master dict.
master_df = pd.concat([master_df, cdc_file], ignore_index=True)
# print(master_df.head(10))


# Add ACS data.

# Function to clean ACS files.
def clean_file(fileCopy, output_filename):
    # Remove rows where the 2nd column is 0
    file = fileCopy.copy()
    file = file[file.iloc[:, 1] != 0]
    total = file.iloc[:, 1]

    # Update each column other than the first two to be a ratio of the total population
    for col in file.columns[2:]:
        file[col] = file[col] / total

    # Apply min-max normalization to all columns except the first one
    cols_to_normalize = file.columns.difference([file.columns[0]])
    file[cols_to_normalize] = file[cols_to_normalize].apply(minmax_normalize)
    file.rename(columns={file.columns[0]: 'zcta'}, inplace=True)
    
    return file
    # Save the cleaned data to the specified filename
    # file.to_csv(output_filename, index=False)


acs_pop_file = pd.read_csv('clean_data/ACS 2020 Table 01 Population.csv')
acs_race_file = pd.read_csv('clean_data/ACS 2020 Table 01 Race.csv')
acs_education_file = pd.read_csv('clean_data/ACS 2020 Table 08 Education.csv')
acs_income_file = pd.read_csv('clean_data/ACS 2020 Table 10 HH Income.csv')
acs_pov_file = pd.read_csv('clean_data/ACS 2020 Table 10 HH Poverty.csv')
acs_insurance_file = pd.read_csv('clean_data/ACS 2020 Table 22 Health Insurance.csv')

# Clean pop file
acs_pop_file = clean_file(acs_pop_file, 'clean_data/Cleaned Pop File.csv')

# Clean race file
acs_race_file = clean_file(acs_race_file, 'clean_data/Cleaned Race File.csv')

# Clean education file
acs_education_file = clean_file(acs_education_file, 'clean_data/Cleaned Education File.csv')

# Clean income file
acs_income_file = clean_file(acs_income_file, 'clean_data/Cleaned Income File.csv')

# Clean poverty file
acs_pov_file = clean_file(acs_pov_file, 'clean_data/Cleaned Poverty File.csv')

# Clean insurance file
acs_insurance_file = clean_file(acs_insurance_file, 'clean_data/Cleaned Insurance File.csv')

# Merge all the cleaned files into one master file, attached by zip code.
# Lose 5 datapoints.
master_df = pd.merge(master_df, acs_pop_file, on='zcta')
master_df = pd.merge(master_df, acs_race_file, on='zcta')
master_df = pd.merge(master_df, acs_education_file, on='zcta')
master_df = pd.merge(master_df, acs_income_file, on='zcta')
master_df = pd.merge(master_df, acs_pov_file, on='zcta')
master_df = pd.merge(master_df, acs_insurance_file, on='zcta')

master_df.rename(columns={'Poverty status in the past 12 months by household type by age of householder, households, total, income in the past 12 months below poverty level': 'poverty_ratio'}, inplace=True)
master_df.to_csv('clean_data/master.csv', index=False)
print(master_df.head(10))
################ Deemed irrelevant!!! ##################################
# Add hospital data.
# hospital_file = pd.read_csv('data/Hospital Compare 2020.csv')

# # Only use zip codes in master file.
# hospital_file['zip_code'] = pd.Categorical(hospital_file['zip_code'], categories=master_df['zcta'].tolist(), ordered=True)
# hospital_file = hospital_file[hospital_file['zip_code'].isin(zcta_list)]

# # Drop 'irrelevant' categories.
# hospital_file.drop(columns=['year', 'hospital_compare_id', 'address', 'city', 'state', 'county_name', 'phone_number'], inplace=True)

# # Deal with hospital duplicates within zip codes.
# hospital_duplicates = hospital_file[hospital_file.duplicated(subset=['zip_code'], keep=False)]
# hospital_duplicates.sort_values(by=['zip_code'], inplace=True, ascending=True, ignore_index=True)

# duplicated_zip_codes = list(set(hospital_duplicates['zip_code'].tolist()))

# hospital_agg_stats = {}
# for zip_code in duplicated_zip_codes:
#     if zip_code == 43016:
#         continue
#     hospital_agg_stats[zip_code] = {}
#     dup_series = hospital_duplicates[hospital_duplicates['zip_code'] == zip_code]
#     for col in dup_series.columns:
#         print(dup_series[col].tolist())

#     exit()

# print(hospital_agg_stats)

# print(len(hospital_file), len(set(hospital_file['zip_code'].tolist())))

#######################################################################################


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


# master_df = pd.DataFrame(master_df_dict)
# # No PR :(
# master_df = master_df[master_df['zcta'] >= 1000]
# # master_df = master_df[master_df['poverty_ratio'] == 1.0]
# # master_df = master_df[master_df['num_households'] > mean_pop]
# # print(len(master_df))
# # print(master_df.head(10))
#
# master_df['norm_pop'] = (master_df['total_population'] - master_df['total_population'].min()) / (master_df['total_population'].max() - master_df['total_population'].min())
# master_df['norm_crude_mhlth'] = (master_df['crude_mhlth'] - master_df['crude_mhlth'].min()) / (master_df['crude_mhlth'].max() - master_df['crude_mhlth'].min())
# master_df['norm_poverty_ratio'] = (master_df['poverty_ratio'] - master_df['poverty_ratio'].min()) / (master_df['poverty_ratio'].max() - master_df['poverty_ratio'].min())
#
# master_df['weighted_score'] = master_df['norm_pop']**0.33 + master_df['norm_crude_mhlth']**0.33 + master_df['norm_poverty_ratio']**0.33
# master_df['weighted_score'] = (master_df['weighted_score'] - master_df['weighted_score'].min()) / (master_df['weighted_score'].max() - master_df['weighted_score'].min())
# master_df.sort_values(by=['weighted_score'], inplace=True, ascending=False, ignore_index=True)
# print(master_df.head(10))
#
#
