import streamlit as st
import pandas as pd

data = {
    "Task Name": ["Math Assignment", "Gym", "Laundry"],
    "Priority": [85, 60, 40],
    "Duration": ["1h 30m", "1h", "30m"]
}

df = pd.DataFrame(data)

st.table(df)
