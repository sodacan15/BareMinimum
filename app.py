import streamlit as st
import pandas as pd

row_labels = ["A", "B", "C"]

data = {
     ["Math Assignment"],
    [85],
    ["1h 30m"]
}

df = pd.DataFrame(data, index = row_labels)

with st.expander("Task: Clean the Room", expanded=False):
    st.table(df)






