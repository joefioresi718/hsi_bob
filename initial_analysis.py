# Importing necessary frameworks
import pandas as pd
import glob

# Using glob to access all ACS files
acs_files = sorted(glob.glob('data/ACS*.csv'))

# Reading in Key: Value pairs in the ACS Data Dictionary
data_dictionary = pd.read_excel('data/ACS Data Dictionary.xlsx')
def_names = {r['Variable']: r['ACS Definition'] for i, r in data_dictionary.iterrows()}
var_list = data_dictionary['Variable'].tolist()

# Updating all of these keys in the original ACS files with their respective values. Saving the new cleaned data to the clean_data folder
for filename in acs_files:
    df = pd.read_csv(filename)
    df.rename(columns=def_names, inplace=True)
    df.to_csv(filename.replace('data', 'clean_data'), index=False)