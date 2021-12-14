import streamlit as st
import pandas as pd

st.title("Moby Bikes Accessibility")
st.sidebar.title("Select")

@st.cache(persist=True)
def load_csv():
    data = pd.read_csv('Moby_November.csv')
    return data

df = load_csv()
