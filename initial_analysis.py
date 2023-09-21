import pandas as pd
import glob


acs_files = glob.glob('data/ACS*.csv')

data_dictionary = pd.read_excel('data/ACS Data Dictionary.xlsx')
print(data_dictionary.head())

var_list = data_dictionary['Variable'].tolist()
 
for filename in acs_files:
    df = pd.read_csv(filename)
    print(df.head())
    exit()