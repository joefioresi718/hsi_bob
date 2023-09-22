import time
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from graphing import minmax_normalize

def center_app():
    st.markdown(
        """
        <style>
            /* Center the app overall */
            .reportview-container .main .block-container {
                display: flex;
                justify-content: center;
                align-items: center;
                flex-direction: column;
                height: 100vh;
            }

            /* Center content inside specific widgets */
            .stButton>button {
                width: 100%;
            }
            .stTextInput>div>div>input {
                width: 100%;
                text-align: center;
            }
            .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown p {
                text-align: center;
            }

            /* For st.text() */
            pre { 
                text-align: center;
                white-space: pre-wrap;   /* Ensure text wraps */
                word-break: break-word;  /* Allow words to break and wrap onto the next line */
            }

            .stContainer {
                text-align: center;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

def add_blank_space(height_in_px=100):
    st.markdown(f"<div style='height:{height_in_px}px;'></div>", unsafe_allow_html=True)

center_app()
st.image('images/SOL Logo Transparent.png')
st.set_option('deprecation.showPyplotGlobalUse', False)

def type_text(message, delay=0.1):
    container = st.empty()
    typed_text = ""
    for char in message:
        typed_text += char
        container.title(typed_text)
        time.sleep(delay)
    return container

type_text("Scroll down and learn more!", delay=0.05)
add_blank_space(300)
def aligned_text(text, alignment='left'):
    st.markdown(f"<p style='text-align: {alignment}; font-weight:bold;'>{text}</p>", unsafe_allow_html=True)

aligned_text("Data driven analysis", "left")
aligned_text("Machine learning for predictive results", "center")
aligned_text("Scaling and bias prevention", "right")
add_blank_space(25)

st.image("images/Relevant Locations.png")
st.subheader("We are launching initial locations based off of U.S. census data")
add_blank_space(25)

st.image("images/Census Graph.png")
st.subheader("Provide correlations using lasso regression")
add_blank_space(50)

st.divider()
st.subheader("Enter your zip code to see your regions results!")

zipcode = st.text_input("")
if zipcode:
    if not zipcode.isdigit():
        st.warning('Please enter a number', icon='⚠️')
    else:
        master_df = pd.read_csv('clean_data/master.csv')
        master_df['weighted_index'] = master_df['poverty_ratio'] ** 0.33 + master_df['totalpopulation'] ** 0.34 + master_df['mhlth_crudeprev'] ** 0.33
        master_df['weighted_index'] = minmax_normalize(master_df['weighted_index'])
        master_df.sort_values(by=['weighted_index'], inplace=True, ascending=False, ignore_index=True)
        categories = ['dental_crudeprev', 'casthma_crudeprev', 'cholscreen_crudeprev', 'csmoking_crudeprev',
                      'depression_crudeprev', 'ghlth_crudeprev', 'Race, total population, total, white alone',
                      'poverty_ratio', 'mhlth_crudeprev']
        category_names = ['Dental', 'Asthma', 'Cholesterol', 'Smoking', 'Depression', 'Poor Physical Health',
                          'White Population', 'Poverty Ratio', 'Poor Mental Health']
        df = master_df[master_df['zcta'] == np.int64(zipcode)]
        if df.empty:
            st.warning('There is no data available for this zipcode', icon='⚠️')
        else:
            df = df.loc[:, categories]
            new_df = pd.DataFrame({'Categories': category_names, 'Values': df.iloc[0]})
            plt.rcParams['axes.labelsize'] = 28
            plt.rcParams['axes.titlesize'] = 32
            plt.rcParams['xtick.labelsize'] = 24
            plt.rcParams['ytick.labelsize'] = 24
            plt.figure(figsize=(14, 10))
            plt.title('Census Statistics for Zip Code ' + str(zipcode))
            sns.barplot(x='Categories', y='Values', data=new_df, palette='Blues_d')
            plt.xticks(rotation=30)
            st.pyplot()

if 'button_pressed' not in st.session_state:
    st.session_state.button_pressed = False
if st.button("Activate Balloons!"):
    st.session_state.button_pressed = True
if st.session_state.button_pressed:
    st.balloons()