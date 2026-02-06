import streamlit as st
import pandas as pd

def task (row, column):
    df = pd.DataFrame(column, index = row, columns=[""])
    with st.expander("Task: Clean the Room", expanded=False):
        st.table(df)


st.markdown("<h1>Hey Mickey</h1>", unsafe_allow_html=True);

row = ["Task Name", "Priority Value", "Duration"]
column = ["Cherry Pie Pikachu", "69", "1 hrs"]

task(row, column)












