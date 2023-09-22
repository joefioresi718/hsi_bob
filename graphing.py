import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


master_df = pd.read_csv('clean_data/master.csv')

dental_crudeprev = -255.95209065009968
casthma_crudeprev = 154.72934271036607
cholscreen_crudeprev = -2.4390530867542486
csmoking_crudeprev = 7.8504999789446455
depression_crudeprev = 24.723082389407598
ghlth_crudeprev = 68.74041508603842
Race_total_population_total_white_alone = -45.37996938016137

data = {
    'categories': ['dental', 'asthma', 'cholestorol_screening', 'smoking', 'depression', 'poor_physical_health', 'white_race'],
    'values': [dental_crudeprev, casthma_crudeprev, cholscreen_crudeprev, csmoking_crudeprev, depression_crudeprev, ghlth_crudeprev, Race_total_population_total_white_alone]
    }
df = pd.DataFrame(data)
df.sort_values(by=['values'], inplace=True, ascending=False, ignore_index=True)

# Create a bar plot.
plt.figure(figsize=(10, 6))
plt.title('Correlation between Census Statistics and Mental Health/Poverty')
# sns.regplot(x='ghlth_crudeprev', y='mhlth_pov_index', data=master_df)
sns.barplot(x='categories', y='values', data=data, order=df['categories'].tolist(), palette='Blues_d')
# Set the x-axis labels diagonal
plt.xticks(rotation=15)
# Remove numbers on the y-axis.
plt.yticks([])
plt.show()

# Normalize column data.
def minmax_normalize(series):
    min_val = series.min()
    max_val = series.max()
    return (series - min_val) / (max_val - min_val)

master_df['weighted_index'] = master_df['poverty_ratio']**0.33 + master_df['totalpopulation']**0.34 + master_df['mhlth_crudeprev']**0.33
master_df['weighted_index'] = minmax_normalize(master_df['weighted_index'])
master_df.sort_values(by=['weighted_index'], inplace=True, ascending=False, ignore_index=True)
# df_melted = df.melt(id_vars="Category", value_vars=["Value_1", "Value_2"], 
#                     var_name="Variable", value_name="Value")

df = master_df.head(5)
df['location'] = ['Tallahassee, FL', 'Bronx (NYC), NY', 'Los Angeles, CA', 'Brownsville, TX', 'Brooklyn, NY']
print(df.loc[:, ['zcta', 'weighted_index', 'totalpopulation', 'mhlth_crudeprev', 'poverty_ratio']])


# Combined index plot.
plt.figure(figsize=(10, 6))
sns.barplot(x='location', y='weighted_index', data=df, palette="viridis", order=df['location'].tolist())
plt.ylim((0.9, 1.0))
plt.title('Top 5 Zip Codes with Highest Weighted Index')
plt.show()

# Combined bar plot.
df = df[['location', 'poverty_ratio', 'mhlth_crudeprev']]
df.rename({'mhlth_crudeprev': 'poor_mental_health'}, axis=1, inplace=True)
df.plot(x='location', kind='bar', figsize=(10, 6), rot=0, colormap='Set1', title='Poverty & Mental Health Issue Ratio per Zip Code', ylabel='Ratio', xlabel='Zip Code')
plt.show()

# Function to plot stats given a zip code.
def plot_regression_values(zip_code, master_df, categories, category_names):
    df = master_df[master_df['zcta'] == zip_code]
    df = df.loc[:, categories]
    new_df = pd.DataFrame({'categories': category_names, 'values': df.iloc[0]})
    print(new_df)
    plt.figure(figsize=(10, 6))
    plt.title('Census Statistics for Zip Code ' + str(zip_code))
    sns.barplot(x='categories', y='values', data=new_df, palette='Blues_d')
    plt.xticks(rotation=15)
    plt.show()

categories = ['dental_crudeprev', 'casthma_crudeprev', 'cholscreen_crudeprev', 'csmoking_crudeprev', 'depression_crudeprev', 'ghlth_crudeprev', 'Race, total population, total, white alone', 'poverty_ratio', 'mhlth_crudeprev']
category_names = ['dental', 'asthma', 'cholestorol_screening', 'smoking', 'depression', 'poor_physical_health', 'white_race', 'poverty_ratio', 'poor_mental_health']

plot_regression_values(34223, master_df, categories, category_names)