import streamlit as st
import pandas as pd

row_labels = ["Task Name", "Priority Value", "Duration"]

data = ["Cherry Pie Pikachu", "69", "1 hrs"]

df = pd.DataFrame(data, index = row_labels, columns=[""])

with st.expander("Task: Clean the Room", expanded=False):
    st.table(df)









