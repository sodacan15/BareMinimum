import streamlit as st
import pandas as pd

# Function to show a task inside an expander
def task(row, column, name):
    df = pd.DataFrame([column], columns=row)
    with st.expander(name, expanded=False):
        st.table(df)

# Sample data for each day
tasks_per_day = {
    "Monday": [
        (["Task Name", "Priority Value", "Duration"], ["Cherry Pie Pikachu", "69", "1 hr"], "Poodle-rama")
    ],
    "Tuesday": [
        (["Task Name", "Priority Value", "Duration"], ["Bulbasaur Smoothie", "45", "2 hrs"], "Leaf Quest")
    ],
    "Wednesday": [
        (["Task Name", "Priority Value", "Duration"], ["Squirtle Splash", "80", "1.5 hrs"], "Water Fun")
    ],
    "Thursday": [
        (["Task Name", "Priority Value", "Duration"], ["Jigglypuff Nap", "20", "3 hrs"], "Sleepy Time")
    ],
    "Friday": [
        (["Task Name", "Priority Value", "Duration"], ["Eevee Party", "55", "2 hrs"], "Weekend Prep")
    ]
}

# Create tabs for the week
tabs = st.tabs(list(tasks_per_day.keys()))

for i, day in enumerate(tasks_per_day.keys()):
    with tabs[i]:
        st.markdown(f"<h2>{day}</h2>", unsafe_allow_html=True)
        st.markdown("<h3>Tasks</h3>", unsafe_allow_html=True)
        for row, column, name in tasks_per_day[day]:
            task(row, column, name)
