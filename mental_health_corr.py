# Importing necessary frameworks
import pandas as pd
import numpy as np

# Load the data into dataframes
cdc_file = pd.read_csv('data/CDC Places 2020 Health Outcomes.csv')
cdc_dict = pd.read_excel('data/CDC Places Data Dictionary.xlsx')
acs_pov_file = pd.read_csv('clean_data/ACS 2020 Table 10 HH Poverty.csv')

# PROCESSING ACS DATA
# Ignore regions with 0 households
acs_pov_file = acs_pov_file[acs_pov_file['Poverty status in the past 12 months by household type by age of householder, households, total'] != 0]

# Extract zip codes
zcta_list = acs_pov_file['Zip code tablulation area (ZCTA)'].tolist()

# Find the poverty ratio (population that has income below poverty : total population)
poverty_ratios = [float(y / x) for x, y in zip(acs_pov_file[
    'Poverty status in the past 12 months by household type by age of householder, households, total'].tolist(), acs_pov_file[
    'Poverty status in the past 12 months by household type by age of householder, households, total, income in the past 12 months below poverty level'
    ].tolist())]

# PROCESSING CDC DATA
# Add in the mental health statistic, clean up data by removing regions with none provided
mhlth_crudeprev = [cdc_file[cdc_file['zcta5'] == zcta]['mhlth_crudeprev'] for zcta in zcta_list]
mhlth_crudeprev = [x.tolist()[0] if len(x) == 1 else None for x in mhlth_crudeprev]

# Pulling in population data through the CDC, clean up data by removing regions with none provided
num_population = [cdc_file[cdc_file['zcta5'] == zcta]['totalpopulation'] for zcta in zcta_list]
num_population = [x.tolist()[0] if len(x) == 1 else 0 for x in num_population]

# Finding the mean population data, this is to help us get an idea of the sizes of these regions
pop_array = np.array(num_population)
mean_pop = pop_array.mean()
print(f'Mean population across zip codes: {mean_pop:.2f}')

# Creating new dataframe to display what we've collected
new_df_dict = {'zcta': zcta_list, 'poverty_ratio': poverty_ratios, 'total_population': num_population, 'crude_mhlth': mhlth_crudeprev}
new_df = pd.DataFrame(new_df_dict)

# No CDC data for Puerto Rico :( (Removing PR zip codes)
new_df = new_df[new_df['zcta'] >= 1000]

# Min-max scaling the population, mental health, and poverty data we've collected
new_df['norm_pop'] = (new_df['total_population'] - new_df['total_population'].min()) / (new_df['total_population'].max() - new_df['total_population'].min())
new_df['norm_crude_mhlth'] = (new_df['crude_mhlth'] - new_df['crude_mhlth'].min()) / (new_df['crude_mhlth'].max() - new_df['crude_mhlth'].min())
new_df['norm_poverty_ratio'] = (new_df['poverty_ratio'] - new_df['poverty_ratio'].min()) / (new_df['poverty_ratio'].max() - new_df['poverty_ratio'].min())

# Using exponential weighting to calculate a score to decide where to initially launch our initiative
new_df['weighted_score'] = new_df['norm_pop']**0.33 + new_df['norm_crude_mhlth']**0.33 + new_df['norm_poverty_ratio']**0.33

# Min-max scaling this weighted score and displaying results
new_df['weighted_score'] = (new_df['weighted_score'] - new_df['weighted_score'].min()) / (new_df['weighted_score'].max() - new_df['weighted_score'].min())
new_df.sort_values(by=['weighted_score'], inplace=True, ascending=False, ignore_index=True)
print(new_df.head(5))




