import streamlit as st
import pandas as pd
from datetime import date, time, datetime, timedelta

st.set_page_config(page_title="Recurring Task Scheduler", layout="wide")

st.title("📅 Recurring Task Scheduler")

# Initialize session state for tasks if not exists
if 'tasks' not in st.session_state:
    st.session_state.tasks = [
        {
            'id': 0,
            'name': 'Computer Programming Terminal App',
            'recurrences': ['Monday', 'Wednesday', 'Friday'],
            'deadline_type': 'Hard',
            'deadline_date': date(2026, 2, 15),
            'time_in': time(9, 0),
            'time_out': time(17, 0),
            'subtasks': [
                {'text': 'Plan the Task', 'done': False},
                {'text': 'Revise the Plan', 'done': False},
                {'text': 'Code the App', 'done': False},
                {'text': 'Check and Revise', 'done': False},
            ],
            'notes': 'Create a terminal-based application with proper error handling and user input validation.',
            'difficulty': 4,
            'event_type': 'Assignment',
            'time_frame': 'All Day'
        }
    ]

# Initialize task counter
if 'task_counter' not in st.session_state:
    st.session_state.task_counter = 1

# ---------- Helper Functions ----------
def calculate_duration(time_in, time_out):
    """Calculate duration between two times"""
    if time_in and time_out:
        dt_in = datetime.combine(date.today(), time_in)
        dt_out = datetime.combine(date.today(), time_out)
        if dt_out < dt_in:
            dt_out += timedelta(days=1)
        duration = dt_out - dt_in
        hours = duration.seconds // 3600
        minutes = (duration.seconds % 3600) // 60
        if hours > 0:
            return f"{hours}h {minutes}m"
        else:
            return f"{minutes}m"
    return "N/A"

def add_new_task():
    """Add a new task with default values"""
    new_task = {
        'id': st.session_state.task_counter,
        'name': 'New Task',
        'recurrences': ['Monday'],
        'deadline_type': 'Hard',
        'deadline_date': date.today() + timedelta(days=7),
        'time_in': time(9, 0),
        'time_out': time(17, 0),
        'subtasks': [
            {'text': 'New subtask', 'done': False},
        ],
        'notes': '',
        'difficulty': 3,
        'event_type': 'Task',
        'time_frame': 'Day'
    }
    st.session_state.tasks.append(new_task)
    st.session_state.task_counter += 1

def delete_task(task_id):
    """Delete a task by ID"""
    st.session_state.tasks = [t for t in st.session_state.tasks if t['id'] != task_id]
    st.rerun()

def remove_recurrence(task_id, recurrence_day):
    """Remove a recurrence day from a task"""
    for task in st.session_state.tasks:
        if task['id'] == task_id:
            if len(task['recurrences']) > 1:  # Keep at least one recurrence
                task['recurrences'] = [d for d in task['recurrences'] if d != recurrence_day]
            break
    st.rerun()

def add_recurrence(task_id, new_day):
    """Add a recurrence day to a task"""
    for task in st.session_state.tasks:
        if task['id'] == task_id:
            if new_day not in task['recurrences'] and len(task['recurrences']) < 7:
                task['recurrences'].append(new_day)
            break

# ---------- Task Renderer ----------
def render_task(task, current_day, task_idx):
    """Renders a single task with all its features"""
    task_id = task['id']
    
    with st.expander(f"📋 {task['name']}", expanded=True):
        
        # ============ RECURRENCE TABS ============
        st.markdown("### 🔄 Recurrence")
        
        # Add new recurrence day selector
        all_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        available_days = [d for d in all_days if d not in task['recurrences']]
        
        if available_days and len(task['recurrences']) < 7:
            col1, col2 = st.columns([3, 1])
            with col1:
                new_day = st.selectbox(
                    "Add recurrence day",
                    ['Select a day...'] + available_days,
                    key=f"add_recur_{task_id}_{current_day}"
                )
            with col2:
                if st.button("➕ Add", key=f"btn_add_recur_{task_id}_{current_day}"):
                    if new_day != 'Select a day...':
                        add_recurrence(task_id, new_day)
                        st.rerun()
        
        st.divider()
        
        # Create tabs for each recurrence day with delete button
        recurrence_tabs = st.tabs([f"{day} ❌" for day in task['recurrences']])
        
        for tab_idx, day in enumerate(task['recurrences']):
            with recurrence_tabs[tab_idx]:
                # Delete button for this recurrence
                if st.button(f"🗑️ Remove {day} recurrence", key=f"del_recur_{task_id}_{day}_{current_day}"):
                    remove_recurrence(task_id, day)
                
                st.divider()
                
                # ============ BASICS SECTION ============
                st.markdown("### 📝 Basics")
                
                # Task name
                task['name'] = st.text_input(
                    "Task Name",
                    value=task['name'],
                    key=f"name_{task_id}_{day}_{current_day}"
                )
                
                # Deadline type
                col1, col2 = st.columns(2)
                with col1:
                    hard_checked = task['deadline_type'] == 'Hard'
                    if st.checkbox("☑️ Hard Deadline", value=hard_checked, key=f"hard_{task_id}_{day}_{current_day}"):
                        task['deadline_type'] = 'Hard'
                    else:
                        task['deadline_type'] = 'Soft'
                
                with col2:
                    soft_checked = task['deadline_type'] == 'Soft'
                    if st.checkbox("☐ Soft Deadline", value=soft_checked, key=f"soft_{task_id}_{day}_{current_day}"):
                        task['deadline_type'] = 'Soft'
                    else:
                        task['deadline_type'] = 'Hard'
                
                # Deadline date
                task['deadline_date'] = st.date_input(
                    "Deadline Date",
                    value=task['deadline_date'],
                    key=f"deadline_{task_id}_{day}_{current_day}"
                )
                
                # Time In and Time Out
                col1, col2, col3 = st.columns([2, 2, 2])
                with col1:
                    task['time_in'] = st.time_input(
                        "⏰ Time In",
                        value=task['time_in'],
                        key=f"time_in_{task_id}_{day}_{current_day}"
                    )
                
                with col2:
                    task['time_out'] = st.time_input(
                        "⏰ Time Out",
                        value=task['time_out'],
                        key=f"time_out_{task_id}_{day}_{current_day}"
                    )
                
                with col3:
                    duration = calculate_duration(task['time_in'], task['time_out'])
                    st.metric("Duration", duration)
                
                st.divider()
                
                # ============ SUB-TASKS SECTION ============
                st.markdown("### ✅ Sub-tasks")
                
                # Render existing subtasks
                for sub_idx, subtask in enumerate(task['subtasks']):
                    col1, col2, col3 = st.columns([1, 5, 1])
                    
                    with col1:
                        subtask['done'] = st.checkbox(
                            "Done",
                            value=subtask['done'],
                            key=f"subtask_done_{task_id}_{day}_{current_day}_{sub_idx}",
                            label_visibility="collapsed"
                        )
                    
                    with col2:
                        subtask['text'] = st.text_input(
                            "Subtask",
                            value=subtask['text'],
                            key=f"subtask_text_{task_id}_{day}_{current_day}_{sub_idx}",
                            label_visibility="collapsed"
                        )
                    
                    with col3:
                        if st.button("🗑️", key=f"del_subtask_{task_id}_{day}_{current_day}_{sub_idx}"):
                            task['subtasks'].pop(sub_idx)
                            st.rerun()
                
                # Add new subtask button
                if st.button("➕ Add Subtask", key=f"add_subtask_{task_id}_{day}_{current_day}"):
                    task['subtasks'].append({'text': 'New subtask', 'done': False})
                    st.rerun()
                
                st.divider()
                
                # ============ NOTES SECTION ============
                st.markdown("### 📓 Notes")
                task['notes'] = st.text_area(
                    "Notes, details, and links",
                    value=task['notes'],
                    height=150,
                    key=f"notes_{task_id}_{day}_{current_day}",
                    placeholder="Add notes, details, links, or reminders here..."
                )
                
                st.divider()
                
                # ============ LOAD-EFFORT SETTINGS ============
                st.markdown("### ⚙️ Load-Effort Settings")
                
                # Difficulty with star rating
                col1, col2 = st.columns([3, 1])
                with col1:
                    difficulty = st.slider(
                        "Difficulty",
                        min_value=1,
                        max_value=5,
                        value=task['difficulty'],
                        key=f"difficulty_{task_id}_{day}_{current_day}"
                    )
                    task['difficulty'] = difficulty
                
                with col2:
                    st.markdown(f"### {'⭐' * difficulty}")
                
                # Event Type
                task['event_type'] = st.selectbox(
                    "Event Type",
                    ['Event', 'Assignment', 'Task', 'Chore'],
                    index=['Event', 'Assignment', 'Task', 'Chore'].index(task['event_type']),
                    key=f"event_type_{task_id}_{day}_{current_day}"
                )
                
                # Time Frame
                task['time_frame'] = st.selectbox(
                    "Time Frame",
                    ['Day', 'Afternoon', 'Evening', 'All Day'],
                    index=['Day', 'Afternoon', 'Evening', 'All Day'].index(task['time_frame']),
                    key=f"time_frame_{task_id}_{day}_{current_day}"
                )
        
        st.divider()
        
        # Delete entire task button
        if st.button(f"🗑️ Delete Task: {task['name']}", key=f"del_task_{task_id}_{current_day}", type="secondary"):
            delete_task(task_id)

# ---------- Build Day Index ----------
week_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
tasks_by_day = {d: [] for d in week_days}

# Populate tasks by day
for idx, task in enumerate(st.session_state.tasks):
    for d in task['recurrences']:
        if d in tasks_by_day:
            tasks_by_day[d].append((idx, task))

# ---------- Top Bar - Add New Task ----------
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    st.markdown("### Manage Your Weekly Tasks")
with col2:
    if st.button("➕ Add New Task", type="primary"):
        add_new_task()
        st.rerun()

st.divider()

# ---------- Render Week Tabs ----------
week_tabs = st.tabs(week_days)

for i, day in enumerate(week_days):
    with week_tabs[i]:
        st.header(f"📅 {day}")
        
        if not tasks_by_day[day]:
            st.info("✨ No tasks scheduled for this day")
        else:
            for task_idx, task in tasks_by_day[day]:
                render_task(task, day, task_idx)
                st.markdown("---")

# ---------- Summary Statistics ----------
st.divider()
st.markdown("### 📊 Weekly Overview")

col1, col2, col3, col4 = st.columns(4)
with col1:
    total_tasks = len(st.session_state.tasks)
    st.metric("Total Tasks", total_tasks)

with col2:
    total_subtasks = sum(len(task['subtasks']) for task in st.session_state.tasks)
    st.metric("Total Subtasks", total_subtasks)

with col3:
    completed_subtasks = sum(
        sum(1 for sub in task['subtasks'] if sub['done']) 
        for task in st.session_state.tasks
    )
    st.metric("Completed Subtasks", completed_subtasks)

with col4:
    avg_difficulty = sum(task['difficulty'] for task in st.session_state.tasks) / total_tasks if total_tasks > 0 else 0
    st.metric("Avg Difficulty", f"{'⭐' * int(avg_difficulty)}")
