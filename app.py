import streamlit as st
from datetime import time
import sys
sys.path.append('.')

from dataStruct import Task, subTask, week

st.set_page_config(page_title="BareMinimum", layout="wide", initial_sidebar_state="expanded")

# Compact dark CSS
st.markdown("""
<style>
    .stApp { background-color: #000; color: #fff; }
    #MainMenu, footer { visibility: hidden; }
    
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&display=swap');
    html, body, [class*="css"] { font-family: 'IBM Plex Mono', monospace; color: #fff; font-size: 12px; }
    
    /* Compact sidebar */
    [data-testid="stSidebar"] { background-color: #000; border-right: 1px solid #fff; min-width: 160px !important; max-width: 160px !important; }
    [data-testid="stSidebar"] > div:first-child { background-color: #000; padding: 1rem 0.5rem; }
    [data-testid="stSidebar"] h1 { font-size: 16px; font-weight: 400; padding: 0.8rem; margin: 0; border-bottom: 1px solid #fff; }
    [data-testid="stSidebar"] .stButton > button {
        background-color: #000; color: #fff; border: 1px solid #fff; border-radius: 0;
        padding: 0.5rem; font-size: 11px; width: 100%; text-align: left; margin-bottom: 0;
    }
    [data-testid="stSidebar"] .stButton > button:hover { background-color: #fff; color: #000; }
    
    /* Main content */
    .main .block-container { padding: 1rem 1.5rem; max-width: 100%; }
    h1, h2, h3 { font-weight: 400; margin: 0; padding: 0; }
    h1 { font-size: 14px; } h2 { font-size: 13px; } h3 { font-size: 12px; }
    
    /* Compact tabs */
    .stTabs [data-baseweb="tab-list"] { gap: 0; background-color: #000; border-bottom: 1px solid #fff; padding: 0; }
    .stTabs [data-baseweb="tab"] {
        background-color: #000; border: 1px solid #fff; border-bottom: none; color: #666;
        padding: 0.4rem 1rem; font-size: 10px; letter-spacing: 0.15em; margin: 0; height: 32px;
    }
    .stTabs [aria-selected="true"] { color: #fff; border-bottom: 1px solid #000; margin-bottom: -1px; }
    
    /* Compact expander */
    .streamlit-expanderHeader {
        background-color: #000; border: 1px solid #fff; color: #fff;
        font-size: 11px; padding: 0.5rem 0.7rem; letter-spacing: 0.03em;
    }
    .streamlit-expanderHeader:hover { background-color: #111; }
    .streamlit-expanderContent {
        background-color: #000; border: 1px solid #fff; border-top: none; padding: 0.8rem 0.7rem; font-size: 11px;
    }
    
    /* Inputs */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select, .stTimeInput > div > div > input {
        background-color: #000; color: #fff; border: 1px solid #fff; border-radius: 0;
        font-size: 11px; padding: 0.3rem 0.5rem;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #000; color: #fff; border: 1px solid #fff; border-radius: 0;
        padding: 0.3rem 0.6rem; font-size: 10px; letter-spacing: 0.1em;
    }
    .stButton > button:hover { background-color: #fff; color: #000; }
    
    /* Checkbox */ .stCheckbox { font-size: 11px; }
    
    /* Compact divider */ hr { border-color: #fff; margin: 0.6rem 0; opacity: 0.3; }
    
    /* Labels */
    .label-text { font-size: 9px; letter-spacing: 0.15em; color: #999; text-transform: uppercase; margin: 0.5rem 0 0.3rem 0; }
    
    /* Progress */ .stProgress > div > div > div { background-color: #fff; height: 3px; }
    
    .stAlert { background-color: #000; border: 1px solid #fff; color: #fff; padding: 0.5rem; font-size: 11px; }
</style>
""", unsafe_allow_html=True)

# Mappings
DIFFICULTY_MAP = {1: "Very Easy", 2: "Easy", 3: "Average", 4: "Hard", 5: "Very Hard"}
EVENT_TAGS = {5: "Event", 4: "Assignment", 3: "Task", 1: "Chore"}
EVENT_TAGS_REVERSE = {v: k for k, v in EVENT_TAGS.items()}
TIME_FRAMES = {1: "Day", 2: "Afternoon", 3: "Evening", 4: "All Day"}
TIME_FRAMES_REVERSE = {v: k for k, v in TIME_FRAMES.items()}

# Initialize
if 'week_instance' not in st.session_state:
    st.session_state.week_instance = week()
    sample = Task()
    sample.setValue("taskName", "TASK 1")
    sample.setValue("taskDifficulty", 4)
    sample.setValue("taskDeadline", 1)
    sample.setValue("timeStart", 540)
    sample.setValue("timeEnd", 1020)
    sample.setValue("eventTag", 4)
    sample.setValue("timeFrame", 4)
    sample.setValue("day", "Monday")
    sample.addSubTask(subTask("Plan", False))
    sample.addSubTask(subTask("Code", False))
    sample.setPriority()
    st.session_state.week_instance.Monday.addTask(sample)
    st.session_state.week_instance.organizeWeek()

if 'task_notes' not in st.session_state:
    st.session_state.task_notes = {}
if 'current_view' not in st.session_state:
    st.session_state.current_view = 'planner'

# Helpers
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
    new_task.addSubTask(subTask("Subtask", False))
    new_task.setPriority()
    day_obj.addTask(new_task)
    st.session_state.week_instance.organizeWeek()

def delete_task(task_name):
    for day in st.session_state.week_instance.days:
        for task in day.tasks[:]:
            if task.taskName == task_name:
                day.removeTask(task)
    if task_name in st.session_state.task_notes:
        del st.session_state.task_notes[task_name]
    st.session_state.week_instance.organizeWeek()

# Compact task renderer
def render_task(task, day_obj, current_day):
    task_key = get_task_key(task)
    
    if task_key not in st.session_state.task_notes:
        st.session_state.task_notes[task_key] = ""
    
    with st.expander(f"{task.taskName}", expanded=False):
        # Name
        st.markdown('<div class="label-text">NAME</div>', unsafe_allow_html=True)
        task.setValue("taskName", st.text_input(
            "n", task.taskName, key=f"n_{task_key}_{id(task)}", label_visibility="collapsed"
        ))
        
        # Deadline type
        c1, c2 = st.columns(2)
        with c1:
            hard = st.checkbox("Hard", task.taskDeadline == 1, key=f"h_{task_key}_{id(task)}")
            task.setValue("taskDeadline", 1 if hard else 0)
        with c2:
            soft = st.checkbox("Soft", task.taskDeadline == 0, key=f"s_{task_key}_{id(task)}", disabled=True)
        
        # Time
        st.markdown('<div class="label-text">TIME</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            tin = st.time_input("In", mins_to_time(task.timeStart), key=f"ti_{task_key}_{id(task)}", label_visibility="collapsed")
            task.setValue("timeStart", time_to_mins(tin))
        with c2:
            tout = st.time_input("Out", mins_to_time(task.timeEnd), key=f"to_{task_key}_{id(task)}", label_visibility="collapsed")
            task.setValue("timeEnd", time_to_mins(tout))
        
        dur = task.taskDuration
        st.text(f"DURATION: {dur//60}h {dur%60}m")
        
        st.divider()
        
        # Subtasks
        st.markdown('<div class="label-text">SUBTASKS</div>', unsafe_allow_html=True)
        st.progress(task.getProgress() / 100)
        
        to_remove = []
        for i, sub in enumerate(task.subTasks):
            c1, c2, c3 = st.columns([1, 7, 1])
            with c1:
                done = st.checkbox("c", sub.status, key=f"sd_{task_key}_{i}_{id(task)}", label_visibility="collapsed")
                if done != sub.status:
                    sub.markDone() if done else sub.markUndone()
            with c2:
                new = st.text_input("t", sub.name, key=f"st_{task_key}_{i}_{id(task)}", label_visibility="collapsed")
                if new != sub.name:
                    sub.name = new
            with c3:
                if st.button("×", key=f"ds_{task_key}_{i}_{id(task)}"):
                    to_remove.append(sub)
        
        for sub in to_remove:
            task.removeSubTask(sub)
        
        if st.button("+ SUBTASK", key=f"as_{task_key}_{id(task)}", use_container_width=True):
            task.addSubTask(subTask("New", False))
            st.rerun()
        
        st.divider()
        
        # Notes
        st.markdown('<div class="label-text">NOTES</div>', unsafe_allow_html=True)
        st.session_state.task_notes[task_key] = st.text_area(
            "notes", st.session_state.task_notes[task_key], height=80,
            key=f"nt_{task_key}_{id(task)}", label_visibility="collapsed",
            placeholder="Notes..."
        )
        
        # Settings (foldable)
        with st.expander("SETTINGS", expanded=False):
            st.markdown('<div class="label-text">BASIC INFORMATION</div>', unsafe_allow_html=True)
            event = st.selectbox(
                "Type", ['Event', 'Assignment', 'Task', 'Chore'],
                index=['Event', 'Assignment', 'Task', 'Chore'].index(EVENT_TAGS.get(task.eventTag, "Task")),
                key=f"et_{task_key}_{id(task)}"
            )
            task.setValue("eventTag", EVENT_TAGS_REVERSE[event])
            
            st.markdown('<div class="label-text">TASK CONFIG</div>', unsafe_allow_html=True)
            diff = st.slider("Difficulty", 1, 5, task.taskDifficulty, key=f"df_{task_key}_{id(task)}")
            task.setValue("taskDifficulty", diff)
        
        if st.button("DELETE", key=f"del_{task_key}_{id(task)}", use_container_width=True):
            delete_task(task_key)
            st.rerun()

# Sidebar
with st.sidebar:
    st.markdown("# BareMinimum")
    st.divider()
    
    if st.button("Planner"):
        st.session_state.current_view = 'planner'
        st.rerun()
    if st.button("Handbook"):
        st.session_state.current_view = 'handbook'
        st.rerun()
    if st.button("Progress"):
        st.session_state.current_view = 'progress'
        st.rerun()

# Main views
if st.session_state.current_view == 'planner':
    # Week tabs at top
    days = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
    days_full = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    tabs = st.tabs(days)
    
    for i, (day_short, day_full) in enumerate(zip(days, days_full)):
        day_obj = st.session_state.week_instance.days[i]
        
        with tabs[i]:
            # Sort by selector (compact)
            st.markdown('<div class="label-text">> SORT BY</div>', unsafe_allow_html=True)
            
            # Priority sections
            if day_obj.highPriority:
                st.markdown("**High Priority**")
                for task in day_obj.highPriority:
                    render_task(task, day_obj, day_full)
            
            if day_obj.mediumPriority:
                st.markdown("**Medium Priority**")
                for task in day_obj.mediumPriority:
                    render_task(task, day_obj, day_full)
            
            if day_obj.smallPriority:
                st.markdown("**Low Priority**")
                for task in day_obj.smallPriority:
                    render_task(task, day_obj, day_full)
            
            if not day_obj.tasks:
                st.info("No tasks")
            
            st.divider()
            if st.button(f"+ ADD TO {day_short}", key=f"add_{day_full}", use_container_width=True):
                add_new_task(day_obj)
                st.rerun()

elif st.session_state.current_view == 'handbook':
    handbook_tabs = st.tabs(["SHORTCUTS", "REMINDERS"])
    
    with handbook_tabs[0]:
        st.markdown('<div class="label-text">DOCS</div>', unsafe_allow_html=True)
        st.text_area("", height=300, placeholder="Links and shortcuts...", key="shortcuts", label_visibility="collapsed")
        if st.button("LINK"):
            st.info("Add link")
    
    with handbook_tabs[1]:
        st.markdown('<div class="label-text">NOTEPAD</div>', unsafe_allow_html=True)
        st.text_area("", height=400, placeholder="Notes...", key="notepad", label_visibility="collapsed")

elif st.session_state.current_view == 'progress':
    total_tasks = sum(len(d.tasks) for d in st.session_state.week_instance.days)
    total_subs = sum(len(t.subTasks) for d in st.session_state.week_instance.days for t in d.tasks)
    done_subs = sum(sum(1 for s in t.subTasks if s.status) for d in st.session_state.week_instance.days for t in d.tasks)
    
    st.text_input("", value=f"{done_subs}/{total_subs} Tasks Done", disabled=True, label_visibility="collapsed")
    
    st.divider()
    st.markdown('<div class="label-text">TASKS</div>', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**In Progress**")
        in_prog = [t for d in st.session_state.week_instance.days for t in d.tasks if 0 < sum(1 for s in t.subTasks if s.status) < len(t.subTasks)]
        if in_prog:
            for t in in_prog:
                st.text(f"• {t.taskName}")
    with c2:
        st.markdown("**Done**")
        done = [t for d in st.session_state.week_instance.days for t in d.tasks if len(t.subTasks) > 0 and all(s.status for s in t.subTasks)]
        if done:
            for t in done:
                st.text(f"• {t.taskName}")
    
    st.divider()
    st.markdown('<div class="label-text">TASKS</div>', unsafe_allow_html=True)
    
    if total_subs > 0:
        progress = (done_subs / total_subs) * 100
        st.progress(progress / 100)
        st.text(f"{progress:.0f}% Complete")
