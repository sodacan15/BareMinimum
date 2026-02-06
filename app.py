import streamlit as st
import pandas as pd

# Function to show a task with a checkbox
def task(row, column, name):
    with st.expander(name, expanded=False):
        # Optional: show task info as a table
        df = pd.DataFrame([column], columns=row)
        st.table(df)

        # Example: subtasks as checkboxes
        checked = []
        checked.append(st.checkbox("Subtask 1", key=f"{name}_sub1"))
        checked.append(st.checkbox("Subtask 2", key=f"{name}_sub2"))
        # You can now use `checked` to see which subtasks are ticked
        st.write("Checked:", checked)

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
