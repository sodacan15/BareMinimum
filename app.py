import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="Weekly Task Tabs", layout="wide")

# ---------- Task Renderer ----------
def task(row, column, name):
    with st.expander(name, expanded=False):

        # Task info table
        df = pd.DataFrame([column], columns=row)
        st.table(df)

        # Done checkbox
        done = st.checkbox("Mark as done ✅", key=f"{name}_done")

        # Date input
        task_date = st.date_input(
            "Task date",
            value=date.today(),
            key=f"{name}_date"
        )

        # ----- Slider + Text Beside It -----
        col1, col2 = st.columns([3, 2])

        with col1:
            rating = st.slider(
                "Task Difficulty ⭐",
                min_value=1,
                max_value=5,
                value=3,
                key=f"{name}_slider"
            )

        rating_text = {
            1: "Very Easy",
            2: "Easy",
            3: "Average",
            4: "Hard",
            5: "Very Hard"
        }

        with col2:
            st.markdown(f"### {'⭐'*rating}")
            st.markdown(f"**{rating_text[rating]}**")


# ---------- Sample Weekly Data ----------
tasks_per_day = {
    "Monday": [
        (["Task Name", "Priority", "Duration"], ["Cherry Pie Pikachu", "69", "1 hr"], "Poodle-rama"),
        (["Task Name", "Priority", "Duration"], ["UI Sketch", "40", "2 hr"], "Wireframe")
    ],
    "Tuesday": [
        (["Task Name", "Priority", "Duration"], ["Bulbasaur Smoothie", "45", "2 hrs"], "Leaf Quest")
    ],
    "Wednesday": [
        (["Task Name", "Priority", "Duration"], ["Backend Logic", "80", "3 hr"], "API Build")
    ],
    "Thursday": [
        (["Task Name", "Priority", "Duration"], ["Refactor", "55", "1.5 hr"], "Code Cleanup")
    ],
    "Friday": [
        (["Task Name", "Priority", "Duration"], ["Deploy", "90", "1 hr"], "Launch")
    ]
}

# ---------- Tabs ----------
tabs = st.tabs(list(tasks_per_day.keys()))

for i, day in enumerate(tasks_per_day.keys()):
    with tabs[i]:
        st.header(day)
        for row, column, name in tasks_per_day[day]:
            task(row, column, name)
