import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
import streamlit as st

from regression import get_model


cmap = sns.color_palette("Blues_r", n_colors=3) + sns.color_palette("YlOrBr", n_colors=7)[:3]

# Inference with model.
def inference(model, values, inference_df):
    inf_df = inference_df.copy()
    # 2, 14, 17, 19, 21, 77
    ext_values = np.zeros(len(inf_df.columns))
    for i, idx in enumerate([2, 14, 17, 19, 21, 77]):
        ext_values[idx] = values[i]
    inf_df.loc[0] = ext_values
    return model.predict(inf_df)/1000


# Plot zipcode data at certain time.
def plot_bardata(model, zipcode, time, zip_dict, inference_df):
    data = zip_dict[zipcode]
    categories = list(data.keys())
    categories.remove('zcta')
    categories.remove('location')
    values = []
    for category in categories:
        values.append(data[category][time])
    
    inf_value = inference(model, values, inference_df)
    values.append(inf_value[0])
    categories = ['Dental', 'Asthma', 'Cholesterol', 'Smoking', 'Poor Health', 'White Race']
    categories.append('Pred MHLTH/POV')
    times = ['Sept. 2023', 'Dec. 2023', 'Mar. 2024', 'Jun. 2024', 'Sept. 2024']
    new_df = pd.DataFrame({'categories': categories, 'values': values})
    plt.figure(figsize=(14, 10))
    plt.rcParams['axes.labelsize'] = 28
    plt.rcParams['axes.titlesize'] = 32
    plt.rcParams['xtick.labelsize'] = 24
    plt.rcParams['ytick.labelsize'] = 24
    plt.xticks(rotation=30)
    plt.title(f'Zip Code {zipcode} Census Statistics on {times[time]}')
    sns.barplot(x='categories', y='values', data=new_df, palette=cmap)
    plt.xlabel(data['location'])
    # plt.show()
    st.pyplot()

# Plot timeseries data for a certain zipcode.
def plot_timeseries(model, zipcode, zip_dict, inference_df):
    data = zip_dict[zipcode]
    categories = list(data.keys())
    categories.remove('zcta')
    categories.remove('location')
    plt.figure(figsize=(14, 10))
    plt.title(f'Zip Code {zipcode} Census Statistics Over Time')
    plt.xlabel('Time')
    plt.rcParams['axes.labelsize'] = 28
    plt.rcParams['axes.titlesize'] = 32
    plt.rcParams['xtick.labelsize'] = 24
    plt.rcParams['ytick.labelsize'] = 24
    plt.xticks(rotation=30)
    # plt.ylabel(category)
    values = []
    for category in categories:
        values.append(data[category])
        plt.plot(data[category], marker='o')
    
    inf_values = []
    for i in range(len(values[0])):
        temp_values = []
        for y in range(len(values)):
            temp_values.append(values[y][i])
        inf_values.append(inference(model, temp_values, inference_df))

    plt.plot(inf_values, linestyle='--', marker='x')
    categories.append('Pred MHLTH/POV')
    plt.legend(categories)
    plt.xticks(np.arange(5), ['Sept. 2023', 'Dec. 2023', 'Mar. 2024', 'Jun. 2024', 'Sept. 2024'])
    # plt.show()
    st.pyplot()


# Create a dictionary of zipcodes and their data.
def get_zip_dict():
    # Load timeseries data.
    df = pd.read_csv('clean_data/example_timeseries.csv')
    print(df)
    zipcodes = df['zcta'].unique()
    zip_dict = {}
    for zipcode in zipcodes:
        df_zipcode = df[df['zcta'] == zipcode]
        dental = df_zipcode['Dental'].tolist()
        asthma = df_zipcode['Asthma'].tolist()
        cholesterol = df_zipcode['Cholesterol'].tolist()
        smoking = df_zipcode['Smoking'].tolist()
        poor_health = df_zipcode['Poor Health'].tolist()
        white_race = df_zipcode['White Race'].tolist()
        zip_dict[zipcode] = {
            'zcta': zipcode,
            'location': df_zipcode['Location'].tolist()[0],
            'dental': dental,
            'asthma': asthma,
            'cholesterol': cholesterol,
            'smoking': smoking,
            'poor_health': poor_health,
            'white_race': white_race
        }
    return zip_dict

if __name__ == '__main__':
    inference_df = pd.read_csv('clean_data/master.csv')
    inference_df = pd.DataFrame(columns=inference_df.columns)
    inference_df.drop(['zcta', 'mhlth_pov_index', 'mhlth_crudeprev', 'poverty_ratio', 'teethlost_crudeprev', 'depression_crudeprev'], axis=1, inplace=True)
    zip_dict = get_zip_dict()
    model = get_model()[0]
    # plot_bardata(model, 32304, 2, zip_dict, inference_df)
    plot_timeseries(model, 10456, zip_dict, inference_df)