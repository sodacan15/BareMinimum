import streamlit as st
import pandas as pd

row_labels = ["A", "B", "C"]

data = {
    "Details": ["Cherry Pie Pikachu", "69", "1 hrs"]
}

df = pd.DataFrame(data, index = row_labels)

with st.expander("Task: Clean the Room", expanded=False):
    st.table(df)







