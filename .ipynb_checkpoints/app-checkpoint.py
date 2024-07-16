import streamlit as st
import pandas as pd
import numpy as np


st.sidebar.header('Olympics Analysis')
st.sidebar.radio('Select an Option',('Medal Tally','OverAll Analysis','Country-wise Analysis','Athlete wise analysis'))

