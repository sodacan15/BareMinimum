import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="Weekly Task Tabs", layout="wide")

# ---------- Task Renderer ----------
def task(row, column, name):
    with st.expander(name, expanded=False):

        tab1, tab2, tab3 = st.tabs(["Info", "Controls", "Difficulty"])

        # ===== TAB 1 — INFO =====
        with tab1:
            df = pd.DataFrame([column], columns=row)
            st.table(df)

        # ===== TAB 2 — CONTROLS =====
        with tab2:
            st.checkbox("Mark as done ✅", key=f"{name}_done")

            st.date_input(
                "Task date",
                value=date.today(),
                key=f"{name}_date"
            )

            c1, c2 = st.columns([1, 3])
            with c1:
                st.markdown("**Deadline Type:**")
            with c2:
                st.radio(
                    "",
                    ["Hard", "Soft"],
                    horizontal=True,
                    key=f"{name}_deadline",
                    label_visibility="collapsed"
                )

        # ===== TAB 3 — DIFFICULTY =====
        with tab3:
            s1, s2 = st.columns([3, 2])

            with s1:
                rating = st.slider(
                    "Task Difficulty ⭐",
                    1, 5, 3,
                    key=f"{name}_slider"
                )

            rating_text = {
                1: "Very Easy",
                2: "Easy",
                3: "Average",
                4: "Hard",
                5: "Very Hard"
            }

            with s2:
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

# ---------- Day Tabs ----------
tabs = st.tabs(list(tasks_per_day.keys()))

for i, day in enumerate(tasks_per_day.keys()):
    with tabs[i]:
        st.header(day)
        for row, column, name in tasks_per_day[day]:
            task(row, column, name)
