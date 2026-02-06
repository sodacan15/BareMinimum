import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="Recurring Task Scheduler", layout="wide")

# ---------- Task Renderer ----------
def render_task(task, day):
    # make widget keys unique per task per day (critical fix)
    key_base = f"{task['name']}_{day}"

    with st.expander(task["name"], expanded=False):

        tab1, tab2, tab3 = st.tabs(["Info", "Controls", "Difficulty"])

        # ===== TAB 1 — INFO =====
        with tab1:
            df = pd.DataFrame([{
                "Category": task["category"],
                "Duration": task["duration"],
                "Deadline": task["deadline"],
                "Recurring": ", ".join(task["days"])
            }])
            st.table(df)

        # ===== TAB 2 — CONTROLS =====
        with tab2:
            st.checkbox("Mark as done ✅", key=f"{key_base}_done")

            st.date_input(
                "Task date",
                value=task["deadline"],
                key=f"{key_base}_date"
            )

            c1, c2 = st.columns([1, 3])
            with c1:
                st.markdown("**Deadline Type:**")
            with c2:
                st.radio(
                    "",
                    ["Hard", "Soft"],
                    horizontal=True,
                    key=f"{key_base}_deadline",
                    label_visibility="collapsed"
                )

        # ===== TAB 3 — DIFFICULTY =====
        with tab3:
            s1, s2 = st.columns([3, 2])

            with s1:
                rating = st.slider(
                    "Task Difficulty ⭐",
                    1, 5,
                    task["difficulty"],
                    key=f"{key_base}_difficulty"
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


# ---------- TASK BUNDLES ----------
# Define once — appears on multiple days automatically

task_bundles = [
    {
        "name": "Algorithm Practice",
        "category": "Coding",
        "deadline": date(2026, 2, 10),
        "duration": "2 hr",
        "difficulty": 4,
        "days": ["Monday", "Wednesday"]
    },
    {
        "name": "Art Commission Sketch",
        "category": "Art",
        "deadline": date(2026, 2, 12),
        "duration": "1.5 hr",
        "difficulty": 3,
        "days": ["Monday"]
    },
    {
        "name": "Backend Refactor",
        "category": "Project",
        "deadline": date(2026, 2, 15),
        "duration": "3 hr",
        "difficulty": 5,
        "days": ["Wednesday"]
    }
]

# ---------- Build Day Index ----------
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
tasks_by_day = {d: [] for d in days}

for task in task_bundles:
    for d in task["days"]:
        if d in tasks_by_day:
            tasks_by_day[d].append(task)

# ---------- Day Tabs ----------
tabs = st.tabs(days)

for i, day in enumerate(days):
    with tabs[i]:
        st.header(day)

        if not tasks_by_day[day]:
            st.info("No tasks scheduled")
        else:
            for task in tasks_by_day[day]:
                render_task(task, day)
