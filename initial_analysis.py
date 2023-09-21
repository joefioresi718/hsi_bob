import pandas as pd
import glob


acs_files = sorted(glob.glob('data/ACS*.csv'))

data_dictionary = pd.read_excel('data/ACS Data Dictionary.xlsx')
print(data_dictionary.head())
def_names = {r['Variable']: r['ACS Definition'] for i, r in data_dictionary.iterrows()}
print(def_names)

var_list = data_dictionary['Variable'].tolist()
 
for filename in acs_files:
    df = pd.read_csv(filename)
    df.rename(columns=def_names, inplace=True)
    df.to_csv(filename.replace('data', 'clean_data'), index=False)
    # print(df.head())