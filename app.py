import streamlit as st
from datetime import time, datetime
import sys
import time as t_lib

sys.path.append('.')

from dataStruct import Task, subTask, week
import functions as fn  # Import backend functions

st.set_page_config(page_title="BareMinimum", layout="wide", initial_sidebar_state="expanded")

# Enhanced dark CSS with completion indicators
st.markdown("""
<style>
    .stApp { background-color: #000; color: #fff; }
    #MainMenu, footer { visibility: hidden; }
    
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&display=swap');
    html, body, [class*="css"] { font-family: 'IBM Plex Mono', monospace; color: #fff; font-size: 12px; }
    
    /* Compact sidebar styling */
    [data-testid="stSidebar"] { 
        background-color: #000; 
        border-right: 1px solid #fff; 
        min-width: 160px !important; 
        max-width: 160px !important; 
    }
    [data-testid="stSidebar"] > div:first-child { background-color: #000; padding: 1rem 0.5rem; }
    [data-testid="stSidebar"] h1 { font-size: 16px; font-weight: 400; padding: 0.8rem; margin: 0; border-bottom: 1px solid #fff; }
    [data-testid="stSidebar"] .stButton > button {
        background-color: #000; color: #fff; border: 1px solid #fff; border-radius: 0;
        padding: 0.5rem; font-size: 11px; width: 100%; text-align: left; margin-bottom: 0;
    }
    [data-testid="stSidebar"] .stButton > button:hover { background-color: #fff; color: #000; }
    
    /* Main content layout */
    .main .block-container { padding: 1rem 1.5rem; max-width: 100%; }
    h1, h2, h3 { font-weight: 400; margin: 0; padding: 0; }
    h1 { font-size: 14px; } h2 { font-size: 13px; } h3 { font-size: 12px; }
    
    /* Compact tabs menu */
    .stTabs [data-baseweb="tab-list"] { gap: 0; background-color: #000; border-bottom: 1px solid #fff; padding: 0; }
    .stTabs [data-baseweb="tab"] {
        background-color: #000; border: 1px solid #fff; border-bottom: none; color: #666;
        padding: 0.4rem 1rem; font-size: 10px; letter-spacing: 0.15em; margin: 0; height: 32px;
    }
    .stTabs [aria-selected="true"] { color: #fff; border-bottom: 1px solid #000; margin-bottom: -1px; }
    
    /* System Inputs */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select, .stTimeInput > div > div > input {
        background-color: #000; color: #fff; border: 1px solid #fff; border-radius: 0;
        font-size: 11px; padding: 0.3rem 0.5rem;
    }
    
    /* Typography and UI Elements */
    .clock-text { font-size: 14px; color: #fff; margin-bottom: 10px; border-bottom: 1px solid #333; padding-bottom: 5px; }
    
    .stButton > button {
        background-color: #000; color: #fff; border: 1px solid #fff; border-radius: 0;
        padding: 0.3rem 0.6rem; font-size: 10px; letter-spacing: 0.1em;
    }
    .stButton > button:hover { background-color: #fff; color: #000; }
    .label-text { font-size: 9px; letter-spacing: 0.15em; color: #999; text-transform: uppercase; margin: 0.5rem 0 0.3rem 0; }
    .stProgress > div > div > div { background-color: #fff; height: 3px; }
    
    /* Custom dividers */
    .custom-divider { 
        border-top: 1px solid #333; 
        margin: 1rem 0; 
    }
    
    /* Task completion indicators */
    .task-complete {
        opacity: 0.5;
        text-decoration: line-through;
    }
    
    .task-status-badge {
        display: inline-block;
        padding: 2px 6px;
        font-size: 8px;
        border: 1px solid;
        margin-left: 5px;
        letter-spacing: 0.1em;
    }
    
    .status-done { border-color: #0f0; color: #0f0; }
    .status-progress { border-color: #ff0; color: #ff0; }
    .status-pending { border-color: #666; color: #666; }
    
    /* Timetable styling */
    .timetable-row {
        display: flex;
        padding: 0.3rem 0.5rem;
        border-bottom: 1px solid #222;
        font-size: 10px;
    }
    
    .timetable-time {
        width: 60px;
        color: #999;
        flex-shrink: 0;
    }
    
    .timetable-task {
        flex-grow: 1;
        padding-left: 1rem;
    }
    
    .timetable-duration {
        width: 50px;
        text-align: right;
        color: #666;
        flex-shrink: 0;
    }
    
    .timetable-header {
        background-color: #111;
        border-top: 1px solid #fff;
        border-bottom: 1px solid #fff;
        padding: 0.5rem;
        font-size: 10px;
        letter-spacing: 0.15em;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Application Mappings
DIFFICULTY_MAP = {1: "Very Easy", 2: "Easy", 3: "Average", 4: "Hard", 5: "Very Hard"}
EVENT_TAGS = {5: "Event", 4: "Assignment", 3: "Task", 1: "Chore"}
EVENT_TAGS_REVERSE = {v: k for k, v in EVENT_TAGS.items()}
TIME_FRAMES = {1: "Day", 2: "Afternoon", 3: "Evening", 4: "All Day"}
TIME_FRAMES_REVERSE = {v: k for k, v in TIME_FRAMES.items()}

# State Initialization
if 'week_instance' not in st.session_state:
    loaded_week = fn.load_tasks()
    if not any(day.tasks for day in loaded_week.days):
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
        loaded_week.Monday.addTask(sample)
        loaded_week.organizeWeek()
    st.session_state.week_instance = loaded_week

# Persistent Storage Initialization
if 'task_notes' not in st.session_state: st.session_state.task_notes = fn.load_notes()
if 'task_recurrences' not in st.session_state: st.session_state.task_recurrences = fn.load_recurrences()
if 'current_view' not in st.session_state: st.session_state.current_view = 'planner'
if 'selected_task_id' not in st.session_state: st.session_state.selected_task_id = None
if 'selected_day' not in st.session_state: st.session_state.selected_day = None
if 'shortcuts' not in st.session_state: st.session_state.shortcuts = fn.load_shortcuts()
if 'handbook_notes' not in st.session_state: st.session_state.handbook_notes = fn.load_handbook_notes()
if 'auto_save' not in st.session_state: st.session_state.auto_save = True
if 'search_filter' not in st.session_state: st.session_state.search_filter = ""

# Helper Functions
def mins_to_time(minutes): return time(minutes // 60, minutes % 60)
def time_to_mins(t): return t.hour * 60 + t.minute

def get_task_status_badge(task):
    """Returns HTML for task status badge"""
    progress = task.getProgress()
    if progress == 100:
        return '<span class="task-status-badge status-done">✓ DONE</span>'
    elif progress > 0:
        return f'<span class="task-status-badge status-progress">{progress:.0f}%</span>'
    else:
        return '<span class="task-status-badge status-pending">TODO</span>'

def get_task_instance_by_name_and_day(task_name, day_name):
    for d in st.session_state.week_instance.days:
        if d.name == day_name:
            for t in d.tasks:
                if t.taskName == task_name:
                    return t
    return None

def add_new_task(day_obj):
    new_task = Task()
    new_task.setValue("taskName", "New Task")
    new_task.setValue("day", day_obj.name)
    new_task.addSubTask(subTask("Subtask", False))
    new_task.setPriority()
    day_obj.addTask(new_task)
    st.session_state.week_instance.organizeWeek()
    if st.session_state.auto_save:
        fn.save_tasks(st.session_state.week_instance)
        fn.save_recurrences(st.session_state.task_recurrences)

def add_recurrence(task_obj, day_name):
    task_name = task_obj.taskName
    if task_name not in st.session_state.task_recurrences:
        st.session_state.task_recurrences[task_name] = []
        
    if day_name not in st.session_state.task_recurrences[task_name]:
        st.session_state.task_recurrences[task_name].append(day_name)
        
        new_task = task_obj.clone() 
        new_task.day = day_name
        
        st.session_state.week_instance.addTaskToDay(new_task, day_name)
        st.session_state.week_instance.organizeWeek()
        
        if st.session_state.auto_save:
            fn.save_tasks(st.session_state.week_instance)

def remove_recurrence(task_name, day_name):
    if task_name in st.session_state.task_recurrences:
        if day_name in st.session_state.task_recurrences[task_name]:
            st.session_state.task_recurrences[task_name].remove(day_name)
            for day in st.session_state.week_instance.days:
                if day.name == day_name:
                    for t in day.tasks[:]:
                        if t.taskName == task_name:
                            day.removeTask(t)
                            break
            st.session_state.week_instance.organizeWeek()
            if st.session_state.auto_save:
                fn.save_tasks(st.session_state.week_instance)
                fn.save_recurrences(st.session_state.task_recurrences)

def get_recurrence_days(task_name):
    if task_name not in st.session_state.task_recurrences:
        st.session_state.task_recurrences[task_name] = []
        for day in st.session_state.week_instance.days:
            for t in day.tasks:
                if t.taskName == task_name:
                    if day.name not in st.session_state.task_recurrences[task_name]:
                        st.session_state.task_recurrences[task_name].append(day.name)
    return st.session_state.task_recurrences[task_name]

def delete_task_by_id(task_id, task_name):
    for day in st.session_state.week_instance.days:
        for t in day.tasks[:]:
            if t.id == task_id:
                day.removeTask(t)
    exists_elsewhere = any(t.taskName == task_name for d in st.session_state.week_instance.days for t in d.tasks)
    if not exists_elsewhere:
        if task_name in st.session_state.task_recurrences: del st.session_state.task_recurrences[task_name]
        if task_name in st.session_state.task_notes: del st.session_state.task_notes[task_name]
    st.session_state.week_instance.organizeWeek()
    if st.session_state.auto_save:
        fn.save_tasks(st.session_state.week_instance)
        fn.save_recurrences(st.session_state.task_recurrences)
        fn.save_notes(st.session_state.task_notes)

def render_task_item(task, day_obj, current_day):
    t_str = mins_to_time(task.timeStart).strftime("%H:%M")
    progress = task.getProgress()
    
    # Create inline status badge with priority percentage
    if progress == 100:
        status_display = f'<span class="task-status-badge status-done">✓ {task.priority}%</span>'
    elif progress > 0:
        status_display = f'<span class="task-status-badge status-progress">{task.priority}% • {progress:.0f}%</span>'
    else:
        status_display = f'<span class="task-status-badge status-pending">{task.priority}%</span>'
    
    button_label = f"[{t_str}] {task.taskName}"
    
    if st.button(button_label, key=f"select_{task.id}", use_container_width=True):
        st.session_state.selected_task_id = task.id
        st.session_state.selected_day = current_day
        st.rerun()
    
    # Display status badge below button
    st.markdown(f'<div style="margin-top:-10px; margin-bottom:10px;">{status_display}</div>', unsafe_allow_html=True)

def render_task_detail(task, day_obj):
    task_key = task.taskName
    if task_key not in st.session_state.task_notes:
        st.session_state.task_notes[task_key] = ""

    recurrence_days = get_recurrence_days(task_key)

    st.markdown(f"### TASK CONFIGURATION")
    
    # Show overall task status
    st.markdown(f'<div style="margin-bottom:1rem;">{get_task_status_badge(task)}</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="label-text">Instance Management</div>', unsafe_allow_html=True)

    all_days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    available_days = [d for d in all_days if d not in recurrence_days]

    if available_days and len(recurrence_days) < 7:
        c1, c2 = st.columns([3,1])
        with c1:
            new_day = st.selectbox(
                "Add instance",
                ['...'] + available_days,
                key=f"add_instance_{task.id}",
                label_visibility="collapsed"
            )
        with c2:
            if st.button("+", key=f"btn_add_instance_{task.id}"):
                if new_day != '...':
                    add_recurrence(task, new_day)
                    st.rerun()

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    instance_tabs = st.tabs([d[:3].upper() for d in recurrence_days])

    for idx, d_name in enumerate(recurrence_days):
        with instance_tabs[idx]:

            inst_task = get_task_instance_by_name_and_day(task_key, d_name)
            if not inst_task:
                st.warning("Instance missing")
                continue

            if len(recurrence_days) > 1:
                if st.button(f"Remove {d_name} instance", key=f"rm_instance_{inst_task.id}_{d_name}"):
                    remove_recurrence(task_key, d_name)
                    st.rerun()
                st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

            settings_tabs = st.tabs(["Main Information", "Subtasks List", "Priority Engine"])

            # ---------- MAIN ----------
            with settings_tabs[0]:
                inst_task.setValue(
                    "taskName",
                    st.text_input("Name", inst_task.taskName,
                                  key=f"n_{inst_task.id}_{d_name}",
                                  label_visibility="collapsed")
                )

                st.markdown('<div class="label-text">Deadline Type</div>', unsafe_allow_html=True)
                hard = st.radio(
                    "dt", ["Hard","Soft"],
                    index=0 if inst_task.taskDeadline == 1 else 1,
                    key=f"deadline_{inst_task.id}_{d_name}",
                    label_visibility="collapsed",
                    horizontal=True
                )
                inst_task.setValue("taskDeadline", 1 if hard=="Hard" else 0)

                st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
                st.markdown('<div class="label-text">Time Window</div>', unsafe_allow_html=True)
                
                c1,c2 = st.columns(2)
                with c1:
                    tin = st.time_input("In", mins_to_time(inst_task.timeStart),
                                        key=f"ti_{inst_task.id}_{d_name}",
                                        label_visibility="collapsed")
                    inst_task.setValue("timeStart", time_to_mins(tin))
                with c2:
                    tout = st.time_input("Out", mins_to_time(inst_task.timeEnd),
                                         key=f"to_{inst_task.id}_{d_name}",
                                         label_visibility="collapsed")
                    inst_task.setValue("timeEnd", time_to_mins(tout))

                st.markdown(f"**DURATION: {inst_task.taskDuration//60}h {inst_task.taskDuration%60}m**")

                st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
                st.markdown('<div class="label-text">Notes</div>', unsafe_allow_html=True)
                
                st.session_state.task_notes[task_key] = st.text_area(
                    "notes",
                    st.session_state.task_notes[task_key],
                    height=100,
                    key=f"nt_{inst_task.id}_{d_name}",
                    label_visibility="collapsed"
                )

            # ---------- SUBTASKS ----------
            with settings_tabs[1]:
                st.progress(inst_task.getProgress() / 100)
                st.markdown(f'**Progress: {inst_task.getProgress():.0f}%**')
                
                st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

                to_remove = []

                for i, sub in enumerate(inst_task.subTasks):
                    u_key = f"{inst_task.id}_{sub.id}_{d_name}_{i}"

                    c1,c2,c3 = st.columns([1,7,1])

                    with c1:
                        done = st.checkbox("c", value=sub.status,
                                           key=f"sd_{u_key}",
                                           label_visibility="collapsed")
                        if done != sub.status:
                            sub.markDone() if done else sub.markUndone()

                    with c2:
                        new_sn = st.text_input("t", value=sub.name,
                                               key=f"st_{u_key}",
                                               label_visibility="collapsed")
                        if new_sn != sub.name:
                            sub.name = new_sn

                    with c3:
                        if st.button("×", key=f"ds_{u_key}"):
                            to_remove.append(sub)

                if to_remove:
                    for sub in to_remove:
                        inst_task.removeSubTask(sub)
                    fn.save_tasks(st.session_state.week_instance)
                    st.rerun()

                st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
                
                if st.button("+ SUBTASK", key=f"as_{inst_task.id}_{d_name}", use_container_width=True):
                    inst_task.addSubTask(subTask("New", False))
                    fn.save_tasks(st.session_state.week_instance)
                    st.rerun()

            # ---------- PRIORITY ----------
            with settings_tabs[2]:
                st.markdown('<div class="label-text">Difficulty Level</div>', unsafe_allow_html=True)
                diff = st.slider("Difficulty", 1,5, inst_task.taskDifficulty,
                                 key=f"df_{inst_task.id}_{d_name}")
                inst_task.setValue("taskDifficulty", diff)

                st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
                st.markdown('<div class="label-text">Event Type</div>', unsafe_allow_html=True)
                
                event = st.selectbox(
                    "Type",
                    ['Event','Assignment','Task','Chore'],
                    index=['Event','Assignment','Task','Chore'].index(
                        EVENT_TAGS.get(inst_task.eventTag,"Task")
                    ),
                    key=f"et_{inst_task.id}_{d_name}"
                )
                inst_task.setValue("eventTag", EVENT_TAGS_REVERSE[event])

                st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
                st.markdown('<div class="label-text">Time Frame</div>', unsafe_allow_html=True)
                
                frame = st.selectbox(
                    "Time Frame",
                    ['Day','Afternoon','Evening','All Day'],
                    index=['Day','Afternoon','Evening','All Day'].index(
                        TIME_FRAMES.get(inst_task.timeFrame,"Day")
                    ),
                    key=f"tf_{inst_task.id}_{d_name}"
                )
                inst_task.setValue("timeFrame", TIME_FRAMES_REVERSE[frame])

                st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
                
                # Recalculate priority (score updates in background)
                inst_task.setPriority()

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    if st.button("💾 Save Task", key=f"save_{task.id}", use_container_width=True):
        st.session_state.week_instance.organizeWeek()
        fn.save_tasks(st.session_state.week_instance)
        fn.save_notes(st.session_state.task_notes)
        fn.save_recurrences(st.session_state.task_recurrences)
        st.success("Saved!")

    if st.button("← Cancel", key=f"cancel_{task.id}", use_container_width=True):
        st.session_state.selected_task_id = None
        st.rerun()

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    
    if st.button("🗑️ Delete Task", key=f"del_{task.id}", use_container_width=True):
        delete_task_by_id(task.id, task_key)
        st.session_state.selected_task_id = None
        st.rerun()

# Sidebar Components
with st.sidebar:
    st.markdown("# BareMinimum")
    st.markdown(f'<div class="clock-text">{datetime.now().strftime("%H:%M:%S")}</div>', unsafe_allow_html=True)
    st.session_state.search_filter = st.text_input("Filter View", value=st.session_state.search_filter, placeholder="Search...")
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    if st.button("📅 Planner"): st.session_state.current_view = 'planner'; st.rerun()
    if st.button("🕒 Timetable"): st.session_state.current_view = 'timetable'; st.rerun()
    if st.button("📖 Handbook"): st.session_state.current_view = 'handbook'; st.rerun()
    if st.button("📊 Progress"): st.session_state.current_view = 'progress'; st.rerun()
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    if st.button("💾 SAVE STATE", use_container_width=True):
        fn.save_tasks(st.session_state.week_instance); fn.save_notes(st.session_state.task_notes)
        fn.save_recurrences(st.session_state.task_recurrences); fn.save_shortcuts(st.session_state.shortcuts)
        fn.save_handbook_notes(st.session_state.handbook_notes); st.success("State Recorded")
    if st.button("📄 EXPORT", use_container_width=True):
        st.download_button("Download .txt", fn.export_to_text(), f"export_{datetime.now().strftime('%Y%m%d')}.txt", "text/plain")
    if st.button("🔄 BACKUP", use_container_width=True): fn.create_backup(); st.success("Backup Successful")
    st.session_state.auto_save = st.checkbox("Auto-save Enabled", value=st.session_state.auto_save, key="auto_save_toggle")

# Main Application Views
if st.session_state.current_view == 'planner':
    col_list, col_detail = st.columns([1, 1])
    with col_list:
        st.markdown('<div class="label-text">> View Sorting</div>', unsafe_allow_html=True)
        sort_choice = st.selectbox("Sort Criteria", ["Priority", "Difficulty", "Time", "Status"], label_visibility="collapsed")
        
        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
        
        days = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
        days_full = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        tabs = st.tabs(days)
        
        for i, (day_short, d_full) in enumerate(zip(days, days_full)):
            day_obj = st.session_state.week_instance.days[i]
            with tabs[i]:
                display_tasks = list(day_obj.tasks)
                
                if sort_choice == "Priority": display_tasks.sort(key=lambda x: x.priority, reverse=True)
                elif sort_choice == "Difficulty": display_tasks.sort(key=lambda x: x.taskDifficulty, reverse=True)
                elif sort_choice == "Time": display_tasks.sort(key=lambda x: x.timeStart)
                elif sort_choice == "Status": display_tasks.sort(key=lambda x: x.getProgress() == 100)
                
                display_tasks = [t for t in display_tasks if st.session_state.search_filter.lower() in t.taskName.lower()]
                if not display_tasks: 
                    st.info("Empty")
                else:
                    last_category = None
                    for t in display_tasks:
                        current_category = None
                        
                        # Define categories based on sort choice
                        if sort_choice == "Priority":
                            if t.priority >= 80: current_category = "HIGH PRIORITY"
                            elif t.priority >= 55: current_category = "MEDIUM PRIORITY"
                            else: current_category = "LOW PRIORITY"
                        elif sort_choice == "Difficulty":
                            if t.taskDifficulty >= 4: current_category = "VERY HARD / HARD"
                            elif t.taskDifficulty == 3: current_category = "AVERAGE"
                            else: current_category = "EASY / VERY EASY"
                        elif sort_choice == "Status":
                            progress = t.getProgress()
                            if progress == 100: current_category = "COMPLETED"
                            elif progress > 0: current_category = "IN PROGRESS"
                            else: current_category = "NOT STARTED"
                        
                        # Show category divider when category changes
                        if current_category and current_category != last_category:
                            st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
                            st.markdown(f'<div class="label-text" style="color:#fff; margin-top:10px; margin-bottom:10px;">{current_category}</div>', unsafe_allow_html=True)
                            last_category = current_category
                        
                        render_task_item(t, day_obj, d_full)
                
                st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
                if st.button(f"+ ADD TO {day_short}", key=f"add_{d_full}", use_container_width=True): 
                    add_new_task(day_obj); st.rerun()
    
    with col_detail:
        if st.session_state.selected_task_id:
            sel_t = next((t for d in st.session_state.week_instance.days for t in d.tasks if t.id == st.session_state.selected_task_id), None)
            if sel_t: render_task_detail(sel_t, None)
            else: st.info("Task Not Found")
        else: st.info("Select Task")

elif st.session_state.current_view == 'timetable':
    st.markdown("### WEEKLY TIMETABLE")
    st.markdown('<div class="label-text">Chronological view of all scheduled tasks</div>', unsafe_allow_html=True)
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    
    days_full = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    for day_name in days_full:
        day_obj = next((d for d in st.session_state.week_instance.days if d.name == day_name), None)
        if day_obj and day_obj.tasks:
            st.markdown(f'<div class="timetable-header">{day_name.upper()}</div>', unsafe_allow_html=True)
            
            # Sort by start time
            sorted_tasks = sorted(day_obj.tasks, key=lambda x: x.timeStart)
            
            for task in sorted_tasks:
                start_time = mins_to_time(task.timeStart).strftime("%H:%M")
                end_time = mins_to_time(task.timeEnd).strftime("%H:%M")
                duration = f"{task.taskDuration//60}h {task.taskDuration%60}m"
                status = get_task_status_badge(task)
                
                st.markdown(f'''
                <div class="timetable-row">
                    <div class="timetable-time">{start_time} - {end_time}</div>
                    <div class="timetable-task">{task.taskName} {status}</div>
                    <div class="timetable-duration">{duration}</div>
                </div>
                ''', unsafe_allow_html=True)
            
            st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

elif st.session_state.current_view == 'handbook':
    handbook_tabs = st.tabs(["SHORTCUTS", "REMINDERS"])
    with handbook_tabs[0]:
        st.markdown('<div class="label-text">EXTERNAL LINKS</div>', unsafe_allow_html=True)
        
        for idx, shortcut in enumerate(st.session_state.shortcuts):
            c1, c2, c3 = st.columns([3, 1, 1])
            with c1: st.text(shortcut["name"])
            with c2: 
                if st.button("Link", key=f"link_{shortcut.get('id', idx)}", use_container_width=True): 
                    st.markdown(f"[{shortcut['name']}]({shortcut['url']})")
            with c3:
                if st.button("Del", key=f"del_shortcut_{shortcut.get('id', idx)}", use_container_width=True):
                    fn.delete_shortcut(shortcut.get('id', idx)); st.session_state.shortcuts = fn.load_shortcuts(); st.rerun()
            st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
        
        with st.expander("+ Create Shortcut"):
            n_name = st.text_input("Site Name", key="new_s_name")
            n_url = st.text_input("URL Path", key="new_s_url")
            if st.button("Save Shortcut"):
                if n_name and n_url: fn.add_shortcut(n_name, n_url); st.session_state.shortcuts = fn.load_shortcuts(); st.rerun()
    
    with handbook_tabs[1]:
        st.markdown('<div class="label-text">CENTRAL NOTEPAD</div>', unsafe_allow_html=True)
        notes = st.text_area("", height=400, value=st.session_state.handbook_notes, key="notepad", label_visibility="collapsed")
        if notes != st.session_state.handbook_notes: st.session_state.handbook_notes = notes; fn.save_handbook_notes(notes)

elif st.session_state.current_view == 'progress':
    tasks = [t for d in st.session_state.week_instance.days for t in d.tasks]
    total_subs = sum(len(t.subTasks) for t in tasks)
    done_subs = sum(sum(1 for s in t.subTasks if s.status) for t in tasks)
    
    st.markdown("### PRODUCTIVITY OVERVIEW")
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    
    st.text_input("", value=f"{done_subs}/{total_subs} Subtasks Completed", disabled=True, label_visibility="collapsed")
    
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Tasks in Focus**")
        in_progress = [t for t in tasks if 0 < sum(1 for s in t.subTasks if s.status) < len(t.subTasks)]
        if not in_progress:
            st.text("• No tasks in progress")
        else:
            for t in in_progress:
                st.text(f"• {t.taskName} ({t.getProgress():.0f}%)")
    
    with c2:
        st.markdown("**Tasks Concluded**")
        completed = [t for t in tasks if len(t.subTasks) > 0 and all(s.status for s in t.subTasks)]
        if not completed:
            st.text("• No completed tasks")
        else:
            for t in completed:
                st.text(f"• {t.taskName}")
    
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    
    if total_subs > 0:
        prog = (done_subs / total_subs) * 100
        st.progress(prog / 100)
        st.text(f"Total Productivity: {prog:.1f}%")

# BareMinimum System Footer - End of Script
