import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="Recurring Task Scheduler", layout="wide")

# ---------- Task Renderer ----------
def render_task(task, current_day):
    """
    Renders a single task with an expander.
    Inside the expander, there is a tab per scheduled day.
    The current_day tab is selected by default.
    """
    days = task["days"]
    name = task["name"]

    with st.expander(name, expanded=False):

        # ---- Shared Info Table ----
        df = pd.DataFrame([{
            "Category": task["category"],
            "Duration": task["duration"],
            "Recurring Days": ", ".join(days)
        }])
        st.table(df)
        st.divider()

        # ---- Inner Tabs for Each Scheduled Day ----
        # Default tab index = current_day
        default_index = days.index(current_day) if current_day in days else 0

        # Create inner tabs
        inner_tabs = st.tabs(days)

        for i, day in enumerate(days):
            key_base = f"{name}_{day}"  # unique key per task per day

            with inner_tabs[i]:
                st.subheader(f"{day} Settings")

                # Done checkbox
                st.checkbox("Mark as done ✅", key=f"{key_base}_done")

                # Task date input
                st.date_input(
                    "Task date",
                    value=task["deadline"],
                    key=f"{key_base}_date"
                )

                # Deadline type (inline)
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

                # Difficulty slider + label
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


# ---------- Task Bundles ----------
# Define tasks once; they appear automatically on scheduled days
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
        "name": "Design Sketching",
        "category": "Art",
        "deadline": date(2026, 2, 12),
        "duration": "1.5 hr",
        "difficulty": 3,
        "days": ["Monday"]
    }
]

# ---------- Build Day Index ----------
week_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
tasks_by_day = {d: [] for d in week_days}

for task in task_bundles:
    for d in task["days"]:
        if d in tasks_by_day:
            tasks_by_day[d].append(task)

# ---------- Render Week Tabs ----------
week_tabs = st.tabs(week_days)

for i, day in enumerate(week_days):
    with week_tabs[i]:
        st.header(day)

        if not tasks_by_day[day]:
            st.info("No tasks scheduled")
        else:
            for task in tasks_by_day[day]:
                render_task(task, day)
