import streamlit as st
from datetime import time
import sys
sys.path.append('.')

# Import the data structures
from dataStruct import Task, subTask, week

# Page config with dark theme
st.set_page_config(page_title="BareMinimum", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS for dark minimalist theme
st.markdown("""
<style>
    /* Main container */
    .stApp {
        background-color: #000000;
        color: #ffffff;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom fonts */
    @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=IBM+Plex+Sans:wght@300;400;500;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'IBM Plex Sans', monospace;
        color: #ffffff;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Space Mono', monospace;
        color: #ffffff;
        font-weight: 700;
        letter-spacing: 0.02em;
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background-color: #0a0a0a;
        border-right: 1px solid #333333;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: transparent;
        color: #ffffff;
        border: 1px solid #ffffff;
        border-radius: 0;
        padding: 0.5rem 1.5rem;
        font-family: 'Space Mono', monospace;
        font-size: 0.85rem;
        letter-spacing: 0.05em;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        background-color: #ffffff;
        color: #000000;
        border-color: #ffffff;
    }
    
    /* Primary buttons */
    .stButton > button[kind="primary"] {
        background-color: #ffffff;
        color: #000000;
        border: 1px solid #ffffff;
    }
    
    .stButton > button[kind="primary"]:hover {
        background-color: transparent;
        color: #ffffff;
    }
    
    /* Input fields */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select,
    .stTimeInput > div > div > input {
        background-color: #000000;
        color: #ffffff;
        border: 1px solid #333333;
        border-radius: 0;
        font-family: 'IBM Plex Sans', sans-serif;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #ffffff;
        box-shadow: none;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: #0a0a0a;
        border: 1px solid #333333;
        border-radius: 0;
        color: #ffffff;
        font-family: 'Space Mono', monospace;
        font-size: 0.95rem;
        padding: 1rem;
    }
    
    .streamlit-expanderHeader:hover {
        background-color: #1a1a1a;
        border-color: #ffffff;
    }
    
    .streamlit-expanderContent {
        background-color: #050505;
        border: 1px solid #333333;
        border-top: none;
        padding: 1.5rem;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background-color: #000000;
        border-bottom: 1px solid #333333;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border: 1px solid #333333;
        border-bottom: none;
        color: #666666;
        padding: 0.75rem 1.5rem;
        font-family: 'Space Mono', monospace;
        font-size: 0.85rem;
        letter-spacing: 0.1em;
        border-radius: 0;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #000000;
        color: #ffffff;
        border-color: #ffffff;
        border-bottom: 1px solid #000000;
    }
    
    /* Divider */
    hr {
        border-color: #333333;
        margin: 1.5rem 0;
    }
    
    /* Checkbox */
    .stCheckbox {
        color: #ffffff;
    }
    
    .stCheckbox > label {
        font-family: 'IBM Plex Sans', sans-serif;
    }
    
    /* Slider */
    .stSlider > div > div > div {
        background-color: #333333;
    }
    
    .stSlider > div > div > div > div {
        background-color: #ffffff;
    }
    
    /* Metric */
    .stMetric {
        background-color: #0a0a0a;
        padding: 1rem;
        border: 1px solid #333333;
    }
    
    .stMetric > label {
        color: #666666;
        font-family: 'Space Mono', monospace;
        font-size: 0.75rem;
        letter-spacing: 0.15em;
    }
    
    .stMetric > div {
        color: #ffffff;
        font-family: 'Space Mono', monospace;
        font-size: 1.5rem;
    }
    
    /* Progress bar */
    .stProgress > div > div > div {
        background-color: #ffffff;
    }
    
    /* Info box */
    .stAlert {
        background-color: #0a0a0a;
        border: 1px solid #333333;
        color: #ffffff;
        border-radius: 0;
    }
    
    /* Section headers */
    .section-header {
        font-family: 'Space Mono', monospace;
        font-size: 0.75rem;
        letter-spacing: 0.2em;
        color: #666666;
        text-transform: uppercase;
        margin-bottom: 1rem;
        border-bottom: 1px solid #333333;
        padding-bottom: 0.5rem;
    }
    
    /* Priority sections */
    .priority-high {
        border-left: 3px solid #ff4444;
        padding-left: 1rem;
        margin-bottom: 2rem;
    }
    
    .priority-medium {
        border-left: 3px solid #ffaa00;
        padding-left: 1rem;
        margin-bottom: 2rem;
    }
    
    .priority-low {
        border-left: 3px solid #44ff44;
        padding-left: 1rem;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Mapping for display
DIFFICULTY_MAP = {1: "Very Easy", 2: "Easy", 3: "Average", 4: "Hard", 5: "Very Hard"}
EVENT_TAGS = {5: "Event", 4: "Assignment", 3: "Task", 1: "Chore"}
EVENT_TAGS_REVERSE = {v: k for k, v in EVENT_TAGS.items()}
TIME_FRAMES = {1: "Day", 2: "Afternoon", 3: "Evening", 4: "All Day"}
TIME_FRAMES_REVERSE = {v: k for k, v in TIME_FRAMES.items()}

# Initialize session state
if 'week_instance' not in st.session_state:
    st.session_state.week_instance = week()
    
    # Create sample task
    sample = Task()
    sample.setValue("taskName", "Computer Programming Terminal App")
    sample.setValue("taskDifficulty", 4)
    sample.setValue("taskDeadline", 1)
    sample.setValue("timeStart", 540)  # 9:00 AM
    sample.setValue("timeEnd", 1020)  # 5:00 PM
    sample.setValue("eventTag", 4)
    sample.setValue("timeFrame", 4)
    sample.setValue("day", "Monday")
    
    sample.addSubTask(subTask("Plan the Task", False))
    sample.addSubTask(subTask("Revise the Plan", False))
    sample.addSubTask(subTask("Code the App", False))
    sample.addSubTask(subTask("Check and Revise", False))
    
    sample.setPriority()
    st.session_state.week_instance.Monday.addTask(sample)
    st.session_state.week_instance.organizeWeek()

if 'task_notes' not in st.session_state:
    st.session_state.task_notes = {}

if 'task_recurrences' not in st.session_state:
    st.session_state.task_recurrences = {}

if 'current_view' not in st.session_state:
    st.session_state.current_view = 'planner'

# ---------- Helper Functions ----------
def mins_to_time(minutes):
    return time(minutes // 60, minutes % 60)

def time_to_mins(t):
    return t.hour * 60 + t.minute

def get_task_key(task):
    return task.taskName

def add_new_task(day_obj):
    new_task = Task()
    new_task.setValue("taskName", "New Task")
    new_task.setValue("day", day_obj.name)
    new_task.addSubTask(subTask("New subtask", False))
    new_task.setPriority()
    day_obj.addTask(new_task)
    st.session_state.task_recurrences[get_task_key(new_task)] = [day_obj.name]
    st.session_state.week_instance.organizeWeek()

def delete_task(task_name):
    for day in st.session_state.week_instance.days:
        for task in day.tasks[:]:
            if task.taskName == task_name:
                day.removeTask(task)
    if task_name in st.session_state.task_recurrences:
        del st.session_state.task_recurrences[task_name]
    if task_name in st.session_state.task_notes:
        del st.session_state.task_notes[task_name]
    st.session_state.week_instance.organizeWeek()

def add_recurrence(task_name, day_name):
    if task_name not in st.session_state.task_recurrences:
        st.session_state.task_recurrences[task_name] = []
    
    if day_name not in st.session_state.task_recurrences[task_name]:
        st.session_state.task_recurrences[task_name].append(day_name)
        
        original = None
        for day in st.session_state.week_instance.days:
            for task in day.tasks:
                if task.taskName == task_name:
                    original = task
                    break
            if original:
                break
        
        if original:
            new_task = Task()
            new_task.setValue("taskName", original.taskName)
            new_task.setValue("taskDifficulty", original.taskDifficulty)
            new_task.setValue("taskDeadline", original.taskDeadline)
            new_task.setValue("timeStart", original.timeStart)
            new_task.setValue("timeEnd", original.timeEnd)
            new_task.setValue("eventTag", original.eventTag)
            new_task.setValue("timeFrame", original.timeFrame)
            new_task.setValue("day", day_name)
            
            for subtask in original.subTasks:
                new_task.addSubTask(subTask(subtask.name, subtask.status))
            
            new_task.setPriority()
            st.session_state.week_instance.addTaskToDay(new_task, day_name)
            st.session_state.week_instance.organizeWeek()

def remove_recurrence(task_name, day_name):
    if task_name in st.session_state.task_recurrences:
        if day_name in st.session_state.task_recurrences[task_name]:
            st.session_state.task_recurrences[task_name].remove(day_name)
            
            for day in st.session_state.week_instance.days:
                if day.name == day_name:
                    for task in day.tasks[:]:
                        if task.taskName == task_name:
                            day.removeTask(task)
                            break
            
            st.session_state.week_instance.organizeWeek()

def get_recurrence_days(task_name):
    if task_name not in st.session_state.task_recurrences:
        st.session_state.task_recurrences[task_name] = []
        for day in st.session_state.week_instance.days:
            for task in day.tasks:
                if task.taskName == task_name:
                    if day.name not in st.session_state.task_recurrences[task_name]:
                        st.session_state.task_recurrences[task_name].append(day.name)
    
    return st.session_state.task_recurrences[task_name]

# ---------- Task Renderer ----------
def render_task(task, day_obj, current_day):
    task_key = get_task_key(task)
    
    if task_key not in st.session_state.task_notes:
        st.session_state.task_notes[task_key] = ""
    
    recurrence_days = get_recurrence_days(task_key)
    
    with st.expander(f"{task.taskName}", expanded=False):
        
        # RECURRENCE SECTION
        st.markdown('<div class="section-header">RECURRENCE</div>', unsafe_allow_html=True)
        
        all_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        available_days = [d for d in all_days if d not in recurrence_days]
        
        if available_days and len(recurrence_days) < 7:
            c1, c2 = st.columns([4, 1])
            with c1:
                new_day = st.selectbox(
                    "Add day",
                    ['...'] + available_days,
                    key=f"add_sel_{task_key}_{current_day}_{id(task)}",
                    label_visibility="collapsed"
                )
            with c2:
                if st.button("ADD", key=f"btn_add_{task_key}_{current_day}_{id(task)}"):
                    if new_day != '...':
                        add_recurrence(task_key, new_day)
                        st.rerun()
        
        st.divider()
        
        # RECURRENCE TABS
        if len(recurrence_days) > 1:
            tabs = st.tabs([f"{d[:3].upper()}" for d in recurrence_days])
        else:
            tabs = st.tabs([d[:3].upper() for d in recurrence_days])
        
        for idx, day in enumerate(recurrence_days):
            with tabs[idx]:
                if len(recurrence_days) > 1:
                    if st.button(f"REMOVE {day}", key=f"rm_{task_key}_{day}_{current_day}_{id(task)}"):
                        remove_recurrence(task_key, day)
                        st.rerun()
                    st.divider()
                
                # BASICS
                st.markdown('<div class="section-header">BASIC INFORMATION</div>', unsafe_allow_html=True)
                
                task.setValue("taskName", st.text_input(
                    "Name", task.taskName, key=f"n_{task_key}_{day}_{current_day}_{id(task)}"
                ))
                
                c1, c2 = st.columns(2)
                with c1:
                    hard = st.checkbox("Hard Deadline", task.taskDeadline == 1, key=f"h_{task_key}_{day}_{current_day}_{id(task)}")
                    task.setValue("taskDeadline", 1 if hard else 0)
                with c2:
                    st.checkbox("Soft Deadline", task.taskDeadline == 0, key=f"s_{task_key}_{day}_{current_day}_{id(task)}", disabled=True)
                
                st.divider()
                
                # TIME
                st.markdown('<div class="section-header">TIME</div>', unsafe_allow_html=True)
                c1, c2, c3 = st.columns(3)
                with c1:
                    tin = st.time_input("Time In", mins_to_time(task.timeStart), key=f"ti_{task_key}_{day}_{current_day}_{id(task)}")
                    task.setValue("timeStart", time_to_mins(tin))
                with c2:
                    tout = st.time_input("Time Out", mins_to_time(task.timeEnd), key=f"to_{task_key}_{day}_{current_day}_{id(task)}")
                    task.setValue("timeEnd", time_to_mins(tout))
                with c3:
                    dur = task.taskDuration
                    st.metric("DURATION", f"{dur//60}h {dur%60}m")
                
                st.divider()
                
                # SUBTASKS
                st.markdown('<div class="section-header">SUBTASKS</div>', unsafe_allow_html=True)
                st.progress(task.getProgress() / 100)
                
                to_remove = []
                for i, sub in enumerate(task.subTasks):
                    c1, c2, c3 = st.columns([1, 6, 1])
                    with c1:
                        done = st.checkbox("", sub.status, key=f"sd_{task_key}_{day}_{current_day}_{i}_{id(task)}", label_visibility="collapsed")
                        if done != sub.status:
                            sub.markDone() if done else sub.markUndone()
                    with c2:
                        new = st.text_input("", sub.name, key=f"st_{task_key}_{day}_{current_day}_{i}_{id(task)}", label_visibility="collapsed")
                        if new != sub.name:
                            sub.name = new
                    with c3:
                        if st.button("DEL", key=f"ds_{task_key}_{day}_{current_day}_{i}_{id(task)}"):
                            to_remove.append(sub)
                
                for sub in to_remove:
                    task.removeSubTask(sub)
                
                if st.button("ADD SUBTASK", key=f"as_{task_key}_{day}_{current_day}_{id(task)}"):
                    task.addSubTask(subTask("New", False))
                    st.rerun()
                
                st.divider()
                
                # NOTES
                st.markdown('<div class="section-header">NOTES</div>', unsafe_allow_html=True)
                st.session_state.task_notes[task_key] = st.text_area(
                    "", st.session_state.task_notes[task_key], height=100,
                    key=f"nt_{task_key}_{day}_{current_day}_{id(task)}", label_visibility="collapsed",
                    placeholder="Add notes, links, or details..."
                )
                
                st.divider()
                
                # SETTINGS
                st.markdown('<div class="section-header">TASK CONFIG</div>', unsafe_allow_html=True)
                
                diff = st.slider("Difficulty", 1, 5, task.taskDifficulty, key=f"df_{task_key}_{day}_{current_day}_{id(task)}")
                task.setValue("taskDifficulty", diff)
                st.markdown(f"### {'⭐' * diff}")
                
                event = st.selectbox(
                    "Type", ['Event', 'Assignment', 'Task', 'Chore'],
                    index=['Event', 'Assignment', 'Task', 'Chore'].index(EVENT_TAGS.get(task.eventTag, "Task")),
                    key=f"et_{task_key}_{day}_{current_day}_{id(task)}"
                )
                task.setValue("eventTag", EVENT_TAGS_REVERSE[event])
                
                frame = st.selectbox(
                    "Time Frame", ['Day', 'Afternoon', 'Evening', 'All Day'],
                    index=['Day', 'Afternoon', 'Evening', 'All Day'].index(TIME_FRAMES.get(task.timeFrame, "Day")),
                    key=f"tf_{task_key}_{day}_{current_day}_{id(task)}"
                )
                task.setValue("timeFrame", TIME_FRAMES_REVERSE[frame])
                
                st.metric("PRIORITY", f"{task.priority}%")
        
        st.divider()
        if st.button(f"DELETE ALL INSTANCES", key=f"del_{task_key}_{current_day}_{id(task)}"):
            delete_task(task_key)
            st.rerun()

# ---------- Main UI ----------

# Sidebar navigation
with st.sidebar:
    st.markdown("# BareMinimum")
    st.divider()
    
    if st.button("Planner", use_container_width=True):
        st.session_state.current_view = 'planner'
        st.rerun()
    
    if st.button("Handbook", use_container_width=True):
        st.session_state.current_view = 'handbook'
        st.rerun()
    
    if st.button("Progress", use_container_width=True):
        st.session_state.current_view = 'progress'
        st.rerun()

# Main content area
if st.session_state.current_view == 'planner':
    # Header
    col1, col2 = st.columns([6, 1])
    with col1:
        st.markdown("# BareMinimum")
    with col2:
        if st.button("NEW TASK", type="primary"):
            add_new_task(st.session_state.week_instance.Monday)
            st.rerun()

    st.divider()

    # Week tabs
    days_short = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
    days_full = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    tabs = st.tabs(days_short)

    for i, (day_short, day_full) in enumerate(zip(days_short, days_full)):
        day_obj = st.session_state.week_instance.days[i]
        
        with tabs[i]:
            if st.button(f"ADD TO {day_short}", key=f"add_{day_full}"):
                add_new_task(day_obj)
                st.rerun()
            
            st.divider()
            
            if not day_obj.tasks:
                st.info(f"No tasks scheduled for {day_full}")
            else:
                if day_obj.highPriority:
                    st.markdown('<div class="priority-high">', unsafe_allow_html=True)
                    st.markdown("**HIGH PRIORITY**")
                    for task in day_obj.highPriority:
                        render_task(task, day_obj, day_full)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                if day_obj.mediumPriority:
                    st.markdown('<div class="priority-medium">', unsafe_allow_html=True)
                    st.markdown("**MEDIUM PRIORITY**")
                    for task in day_obj.mediumPriority:
                        render_task(task, day_obj, day_full)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                if day_obj.smallPriority:
                    st.markdown('<div class="priority-low">', unsafe_allow_html=True)
                    st.markdown("**LOW PRIORITY**")
                    for task in day_obj.smallPriority:
                        render_task(task, day_obj, day_full)
                    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.current_view == 'handbook':
    st.markdown("# Handbook")
    st.divider()
    
    handbook_tabs = st.tabs(["SHORTCUTS", "REMINDERS"])
    
    with handbook_tabs[0]:
        st.markdown('<div class="section-header">DOCS</div>', unsafe_allow_html=True)
        st.text_area("", height=300, placeholder="Add your shortcuts, links, and quick references here...", key="shortcuts_area")
        if st.button("LINK", key="add_shortcut"):
            st.info("Add link functionality here")
    
    with handbook_tabs[1]:
        st.markdown('<div class="section-header">NOTEPAD</div>', unsafe_allow_html=True)
        st.text_area("", height=400, placeholder="Write your notes and reminders here...", key="reminders_area")

elif st.session_state.current_view == 'progress':
    st.markdown("# Progress")
    st.divider()
    
    # Calculate stats
    total_tasks = sum(len(d.tasks) for d in st.session_state.week_instance.days)
    total_subtasks = sum(len(t.subTasks) for d in st.session_state.week_instance.days for t in d.tasks)
    done_subtasks = sum(sum(1 for s in t.subTasks if s.status) for d in st.session_state.week_instance.days for t in d.tasks)
    
    st.text_input("", value=f"{done_subtasks}/{total_subtasks} Tasks Done", key="progress_display", disabled=True)
    
    st.divider()
    
    st.markdown('<div class="section-header">TASKS</div>', unsafe_allow_html=True)
    
    # Progress/Done columns
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**In Progress**")
        in_progress = [t for d in st.session_state.week_instance.days for t in d.tasks if not all(s.status for s in t.subTasks) and any(s.status for s in t.subTasks)]
        if in_progress:
            for task in in_progress:
                st.text(f"• {task.taskName}")
        else:
            st.text("No tasks in progress")
    
    with col2:
        st.markdown("**Done**")
        done_tasks = [t for d in st.session_state.week_instance.days for t in d.tasks if all(s.status for s in t.subTasks) and len(t.subTasks) > 0]
        if done_tasks:
            for task in done_tasks:
                st.text(f"• {task.taskName}")
        else:
            st.text("No completed tasks")
    
    st.divider()
    
    st.markdown('<div class="section-header">TASKS</div>', unsafe_allow_html=True)
    
    # Progress bar visualization
    if total_subtasks > 0:
        progress_percentage = (done_subtasks / total_subtasks) * 100
        st.progress(progress_percentage / 100)
        st.markdown(f"**{progress_percentage:.1f}% Complete**")
    else:
        st.info("No tasks to track")

# Footer stats (always visible)
st.divider()
st.markdown('<div class="section-header">OVERVIEW</div>', unsafe_allow_html=True)

total = sum(len(d.tasks) for d in st.session_state.week_instance.days)
subs = sum(len(t.subTasks) for d in st.session_state.week_instance.days for t in d.tasks)
done = sum(sum(1 for s in t.subTasks if s.status) for d in st.session_state.week_instance.days for t in d.tasks)

c1, c2, c3 = st.columns(3)
with c1:
    st.metric("TASKS", total)
with c2:
    st.metric("SUBTASKS", subs)
with c3:
    st.metric("DONE", f"{done}/{subs}")
