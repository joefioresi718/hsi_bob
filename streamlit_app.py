import time
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from graphing import minmax_normalize
from model_inference import get_model, inference, plot_bardata, plot_timeseries, get_zip_dict


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

def type_script(message, delay=0.1):
    container = st.empty()
    typed_text = "Report: "
    for char in message:
        typed_text += char
        container.caption(typed_text)
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

@st.cache_resource
def get_inf_model():
    model = get_model()[0]
    zip_dict = get_zip_dict()
    # Get ready for inference columns.
    inference_df = pd.read_csv('clean_data/master.csv')
    inference_df = pd.DataFrame(columns=inference_df.columns)
    inference_df.drop(['zcta', 'mhlth_pov_index', 'mhlth_crudeprev', 'poverty_ratio', 'teethlost_crudeprev', 'depression_crudeprev'], axis=1, inplace=True)
    return model, zip_dict, inference_df

model, zip_dict, inference_df = get_inf_model()
zip_locations = [zip_dict[zip_code]["location"] for zip_code in zip_dict.keys()]
zcode = st.selectbox("Select a zip code", zip_dict.keys(), format_func=lambda x: f'{zip_dict[x]["location"]} - {x}')
if zcode:
    disp_timestep = ['Sept. 2023', 'Dec. 2023', 'Mar. 2024', 'Jun 2024', 'Sept 2024']
    timestep = st.selectbox("Select a timestep", np.arange(5), format_func=lambda x: disp_timestep[x])
    plot_bardata(model, zcode, timestep, zip_dict, inference_df)
    plot_timeseries(model, zcode, zip_dict, inference_df)

scripts = {
    32304: "This zip code is located in Tallahassee, Florida. It has a high poverty ratio, and a high mental health issue ratio. Across time, the various contributing factors seem to waver without consistently improving or declining. This indicates that more focus should be placed on this zip code to help improve the mental health of its residents. Consider focusing on improving the dental health of the residents, as this is the most significant factor in the mental health issue ratio.",
    10456: "This zip code is located in the Bronx (NYC), NY. Compared to other areas, the Bronx has a particularly diverse population. However, it has an unusually high ratio of asthmatics and people with poor physical health. That being said, across the past year, these factors have drastically improved, leading to a decreased risk of mental health issues.",
    90011: "This zip code is located in Los Angeles, CA. This region has particularly low access to dental care, and a higher ratio of people with low physical health. These factors have seen only minor improvement over the past year. Consider applying more focus on the general physical health of the residents.",
    98052: "This zip code is located in Redmond, WA. This region had a low poverty mental-health index around Sept. 2023, but has experienced significant decline in each of the major correlated factors since. This may be due to the (hypothetical) departure of a major employer in the area. Without said employer incentivising proper physical and mental care, this region has seen a decline. The residents have been calling for the return of this employer in an effort to restore balance to Redmond, WA.",
}
report_button = st.button("Generate Report")
if report_button:
    script = scripts[zcode]
    type_script(script, delay=0.02)
    # st.markdown(script, unsafe_allow_html=True)


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