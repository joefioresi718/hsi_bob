# Importing pandas for data processing
import pandas as pd

# Reading in our CDC data and dictionary
cdc = pd.read_csv('data/CDC Places 2020 Health Outcomes.csv')
dict = pd.read_excel('data/CDC Places Data Dictionary.xlsx')

# Creating a dictionary of the abbreviated data points to their measure, unit, and definition
mapping_dict = {}

for _, row in dict.iterrows():
    key = row['Variable']
    value = f"{row['Measure']} | {row['Units']} | {row['Definition']}"
    mapping_dict[key] = value

# Applying this dictionary value to the column titles using their current keys
cdc.columns = [mapping_dict.get(col, col) for col in cdc.columns]

# Extracing the data specific to the mental health problems
mental_health_col = [col for col in cdc.columns if "mental health" in col.lower()][0]

# Creating our new dataframe to order columns and sort by mental health data
new_cdc = cdc[['ZCTA | label | Zip code tabulation area (ZCTA)','crude prevalence rate | per 1000 | Model-based estimate for crude prevalence of mental health not good for >=14 days among adults aged >=18 years, 2020', 'population | individuals | Total Population of Census 2010']]
new_cdc = new_cdc.sort_values(by='crude prevalence rate | per 1000 | Model-based estimate for crude prevalence of mental health not good for >=14 days among adults aged >=18 years, 2020', ascending=False)

# Extracting our zip code index
zip_codes = pd.read_excel('data/Zip Code Index.xlsx')

# Creating a new column to specify the city and state of the zip code
zip_codes['city_state'] = zip_codes['po_name'] + ", " + zip_codes['state_name']

# Merging our resulting sorted table with its specific city and state location
merged_df = pd.merge(new_cdc, zip_codes[['zip_code', 'city_state']], left_on='ZCTA | label | Zip code tabulation area (ZCTA)', right_on='zip_code', how='left')
merged_df.drop(['ZCTA | label | Zip code tabulation area (ZCTA)', 'zip_code'], axis=1, inplace=True)
merged_df.rename(columns={'city_state': 'Location'}, inplace=True)

# Saving and displaying data
merged_df.to_csv('clean_data/CDC Mental Health Data.csv')
print(merged_df.head(10))

