import streamlit as st
import pandas as pd

def task (row, column, name):
    df = pd.DataFrame(column, index = row, columns=[""])
    with st.expander(name, expanded=False):
        st.table(df)

row = ["Task Name", "Priority Value", "Duration"]
column = ["Cherry Pie Pikachu", "69", "1 hrs"]

st.markdown("<h2>Monday</h2>", unsafe_allow_html=True);
st.markdown("<h3>Low Priority</h3>", unsafe_allow_html=True);
task(row, column, "Poodle-rama")













