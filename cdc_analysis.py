import pandas as pd
import numpy as np
import matplotlib as plt

cdc = pd.read_csv('data/CDC Places 2020 Health Outcomes.csv')
dict = pd.read_excel('data/CDC Places Data Dictionary.xlsx')

mapping_dict = {}

for _, row in dict.iterrows():
    key = row['Variable']
    value = f"{row['Measure']} | {row['Units']} | {row['Definition']}"
    mapping_dict[key] = value

cdc.columns = [mapping_dict.get(col, col) for col in cdc.columns]

mental_health_col = [col for col in cdc.columns if "mental health" in col.lower()][0]

new_cdc = cdc[['ZCTA | label | Zip code tabulation area (ZCTA)','crude prevalence rate | per 1000 | Model-based estimate for crude prevalence of mental health not good for >=14 days among adults aged >=18 years, 2020', 'population | individuals | Total Population of Census 2010']]
new_cdc = new_cdc.sort_values(by='crude prevalence rate | per 1000 | Model-based estimate for crude prevalence of mental health not good for >=14 days among adults aged >=18 years, 2020', ascending=False)

zip_codes = pd.read_excel('data/Zip Code Index.xlsx')

zip_codes['city_state'] = zip_codes['po_name'] + ", " + zip_codes['state_name']

merged_df = pd.merge(new_cdc, zip_codes[['zip_code', 'city_state']], left_on='ZCTA | label | Zip code tabulation area (ZCTA)', right_on='zip_code', how='left')

merged_df.drop(['ZCTA | label | Zip code tabulation area (ZCTA)', 'zip_code'], axis=1, inplace=True)

merged_df.rename(columns={'city_state': 'Location'}, inplace=True)

merged_df.to_csv('new_cdc.csv')

