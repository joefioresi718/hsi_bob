import streamlit as st
import pandas as pd
import numpy as np


st.title("Altura")
st.subheader(":blue[*Heighten*] your intentions with your data.")
# st.divider()
st.title("")

col1, col2, col3 = st.columns(3)
col1.metric("Left", "∞", "∞")
col2.metric("Center", "∞", "∞")
col3.metric("Right", "∞", "∞")

df = pd.DataFrame(
    np.random.randn(50, 2) / [0.1, 0.1] + [41.537030, -97.485650],
    columns=['lat', 'lon'])

st.map(df,
       size='None',
       color='#ffffff',
       zoom=4)