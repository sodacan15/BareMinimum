import streamlit as st
import pandas as pd
from datetime import date

# Function to show a task with checkbox and date input
def task(row, column, name):
    with st.expander(name, expanded=False):
        # Display task info as a table
        df = pd.DataFrame([column], columns=row)
        st.table(df)

        # Subtasks as checkboxes
        checked = []
        checked.append(st.checkbox("Subtask 1", key=f"{name}_sub1"))
        checked.append(st.checkbox("Subtask 2", key=f"{name}_sub2"))

        # Date input for this task
        task_date = st.date_input("Select task date", value=date.today(), key=f"{name}_date")

        rating = st.radio(
            "Rate this task ⭐",
            options=[1, 2, 3, 4, 5],
            format_func=lambda x: "⭐" * x,
            key=f"{name}_rating"
        )

# Sample data for each day
tasks_per_day = {
    "Monday": [
        (["Task Name", "Priority Value", "Duration"], ["Cherry Pie Pikachu", "69", "1 hr"], "Poodle-rama")
    ],
    "Tuesday": [
        (["Task Name", "Priority Value", "Duration"], ["Bulbasaur Smoothie", "45", "2 hrs"], "Leaf Quest")
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

