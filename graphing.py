import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap

# Create a colormap with just two colors: blue and yellow
colors = [(0, 'tab:blue'), (1, 'gold')]
cmap_name = 'blue_yellow'
blue_yellow = LinearSegmentedColormap.from_list(cmap_name, colors)

master_df = pd.read_csv('clean_data/master.csv')
cmap = sns.color_palette("Blues_r", n_colors=3) + sns.color_palette("YlOrBr", n_colors=7)[:3]

dental_crudeprev = -260.1234740089023
casthma_crudeprev = 169.0422638032042 
cholscreen_crudeprev = -3.8168575344060063
csmoking_crudeprev = 16.68021834248791
ghlth_crudeprev = 65.52371230460604
Race_total_population_total_white_alone = -38.97065106719211

data = {
    'categories': ['Dental', 'Asthma', 'Cholesterol', 'Smoking', 'Poor Health', 'White Race'],
    'values': [dental_crudeprev, casthma_crudeprev, cholscreen_crudeprev, csmoking_crudeprev, ghlth_crudeprev, Race_total_population_total_white_alone]
    }
df = pd.DataFrame(data)
df.sort_values(by=['values'], inplace=True, ascending=False, ignore_index=True)

plt.rcParams['axes.labelsize'] = 28
plt.rcParams['axes.titlesize'] = 21
plt.rcParams['xtick.labelsize'] = 20
plt.figure(figsize=(10, 14))
plt.title('Correlation between Census Statistics and Mental Health/Poverty')
sns.barplot(x='categories', y='values', data=data, order=df['categories'].tolist(), palette=cmap)
plt.xticks(rotation=25)
plt.yticks([])
plt.savefig("images/Graph 1.png")


def minmax_normalize(series):
    min_val = series.min()
    max_val = series.max()
    return (series - min_val) / (max_val - min_val)

master_df['weighted_index'] = master_df['poverty_ratio']**0.33 + master_df['totalpopulation']**0.34 + master_df['mhlth_crudeprev']**0.33
master_df['weighted_index'] = minmax_normalize(master_df['weighted_index'])
master_df.sort_values(by=['weighted_index'], inplace=True, ascending=False, ignore_index=True)

df = master_df.head(5)
df['location'] = ['Tallahassee, FL', 'Bronx (NYC), NY', 'Los Angeles, CA', 'Brownsville, TX', 'Brooklyn, NY']


plt.figure(figsize=(12, 12))
plt.rcParams['axes.labelsize'] = 28
plt.rcParams['axes.titlesize'] = 28
plt.rcParams['xtick.labelsize'] = 20
plt.rcParams['ytick.labelsize'] = 24
plt.xticks(rotation=10)
sns.barplot(x='location', y='weighted_index', data=df, palette=cmap, order=df['location'].tolist())
plt.ylim((0.9, 1.0))
plt.title('Top 5 Zip Codes with Highest Weighted Index')
plt.savefig("images/Graph 2.png")

df = df[['location', 'poverty_ratio', 'mhlth_crudeprev']]
df.rename({'mhlth_crudeprev': 'poor_mental_health'}, axis=1, inplace=True)
df.plot(x='location', kind='bar', figsize=(10, 6), rot=0, colormap=blue_yellow, title='Poverty & Mental Health Issue Ratio per Zip Code', ylabel='Ratio', xlabel='Zip Code')
plt.savefig("images/Graph 3.png")

def plot_regression_values(zip_code, master_df, categories, category_names):
    df = master_df[master_df['zcta'] == zip_code]
    df = df.loc[:, categories]
    new_df = pd.DataFrame({'categories': category_names, 'values': df.iloc[0]})
    plt.figure(figsize=(10, 6))
    plt.title('Census Statistics for Zip Code ' + str(zip_code))
    sns.barplot(x='categories', y='values', data=new_df, palette=cmap)
    plt.xticks(rotation=17)
    plt.savefig("images/Graph 4.png")

categories = ['dental_crudeprev', 'casthma_crudeprev', 'cholscreen_crudeprev', 'csmoking_crudeprev', 'ghlth_crudeprev', 'Race, total population, total, white alone', 'poverty_ratio', 'mhlth_crudeprev']
category_names = ['dental', 'asthma', 'cholestorol_screening', 'smoking', 'poor_physical_health', 'white_race', 'poverty_ratio', 'poor_mental_health']

plot_regression_values(78701, master_df, categories, category_names)