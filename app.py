import streamlit as st
from datetime import time, datetime
import sys
sys.path.append('.')

from dataStruct import Task, subTask, week
import functions as fn  # Import backend functions

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
    # Try to load from JSON, otherwise create sample
    loaded_week = fn.load_tasks()
    if not any(day.tasks for day in loaded_week.days):
        # No tasks loaded, create sample
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

if 'task_notes' not in st.session_state:
    st.session_state.task_notes = fn.load_notes()
if 'task_recurrences' not in st.session_state:
    st.session_state.task_recurrences = fn.load_recurrences()
if 'current_view' not in st.session_state:
    st.session_state.current_view = 'planner'
if 'selected_task' not in st.session_state:
    st.session_state.selected_task = None
if 'selected_day' not in st.session_state:
    st.session_state.selected_day = None
if 'shortcuts' not in st.session_state:
    st.session_state.shortcuts = fn.load_shortcuts()
if 'handbook_notes' not in st.session_state:
    st.session_state.handbook_notes = fn.load_handbook_notes()
if 'auto_save' not in st.session_state:
    st.session_state.auto_save = True

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
    # Auto-save to JSON
    if st.session_state.auto_save:
        fn.save_tasks(st.session_state.week_instance)
        fn.save_recurrences(st.session_state.task_recurrences)

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
            
            # Auto-save to JSON
            if st.session_state.auto_save:
                fn.save_tasks(st.session_state.week_instance)
                fn.save_recurrences(st.session_state.task_recurrences)

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
            
            # Auto-save to JSON
            if st.session_state.auto_save:
                fn.save_tasks(st.session_state.week_instance)
                fn.save_recurrences(st.session_state.task_recurrences)

def get_recurrence_days(task_name):
    if task_name not in st.session_state.task_recurrences:
        st.session_state.task_recurrences[task_name] = []
        for day in st.session_state.week_instance.days:
            for task in day.tasks:
                if task.taskName == task_name:
                    if day.name not in st.session_state.task_recurrences[task_name]:
                        st.session_state.task_recurrences[task_name].append(day.name)
    
    return st.session_state.task_recurrences[task_name]

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
    
    # Auto-save to JSON
    if st.session_state.auto_save:
        fn.save_tasks(st.session_state.week_instance)
        fn.save_recurrences(st.session_state.task_recurrences)
        fn.save_notes(st.session_state.task_notes)

# Compact task renderer - clickable list item
def render_task_item(task, day_obj, current_day):
    task_key = get_task_key(task)
    
    # Simple clickable task item
    if st.button(f"{task.taskName} >", key=f"select_{task_key}_{current_day}", use_container_width=True):
        st.session_state.selected_task = task_key
        st.session_state.selected_day = current_day
        st.rerun()

# Task detail panel (right side)
def render_task_detail(task, day_obj):
    task_key = get_task_key(task)
    
    if task_key not in st.session_state.task_notes:
        st.session_state.task_notes[task_key] = ""
    
    recurrence_days = get_recurrence_days(task_key)
    
    st.markdown(f"### TASK")
    
    # Instance with day tabs
    st.markdown('<div class="label-text">Instance</div>', unsafe_allow_html=True)
    
    # Show existing instances + add button
    all_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    available_days = [d for d in all_days if d not in recurrence_days]
    
    # Add new instance selector
    if available_days and len(recurrence_days) < 7:
        c1, c2 = st.columns([3, 1])
        with c1:
            new_day = st.selectbox(
                "Add instance to day",
                ['...'] + available_days,
                key=f"add_instance_{task_key}",
                label_visibility="collapsed"
            )
        with c2:
            if st.button("+", key=f"btn_add_instance_{task_key}"):
                if new_day != '...':
                    add_recurrence(task_key, new_day)
                    st.rerun()
    
    st.divider()
    
    # Tabs for each instance
    if len(recurrence_days) > 1:
        instance_tabs = st.tabs([f"{d[:3].upper()}" for d in recurrence_days])
    else:
        instance_tabs = st.tabs([d[:3].upper() for d in recurrence_days])
    
    for idx, day in enumerate(recurrence_days):
        with instance_tabs[idx]:
            # Remove instance button if more than one
            if len(recurrence_days) > 1:
                if st.button(f"Remove {day} instance", key=f"rm_instance_{task_key}_{day}"):
                    remove_recurrence(task_key, day)
                    st.rerun()
                st.divider()
            
            # SETTINGS - Nested tabs within this instance
            settings_tabs = st.tabs(["Basic Information", "Subtasks", "Task Config"])
            
            # Tab 1: Basic Information
            with settings_tabs[0]:
                # Name
                st.markdown('<div class="label-text">NAME</div>', unsafe_allow_html=True)
                task.setValue("taskName", st.text_input(
                    "Name", task.taskName, key=f"n_{task_key}_{day}_{id(task)}", 
                    label_visibility="collapsed"
                ))
                
                # Deadline type
                st.markdown('<div class="label-text">Deadline Type</div>', unsafe_allow_html=True)
                c1, c2 = st.columns(2)
                with c1:
                    hard = st.radio("dt", ["Hard", "Soft"], index=0 if task.taskDeadline == 1 else 1, 
                                   key=f"deadline_{task_key}_{day}_{id(task)}", label_visibility="collapsed", horizontal=True)
                    task.setValue("taskDeadline", 1 if hard == "Hard" else 0)
                
                # Time
                st.markdown('<div class="label-text">TIME IN / TIME OUT</div>', unsafe_allow_html=True)
                c1, c2 = st.columns(2)
                with c1:
                    tin = st.time_input("Time In", mins_to_time(task.timeStart), key=f"ti_{task_key}_{day}_{id(task)}", 
                                       label_visibility="collapsed")
                    task.setValue("timeStart", time_to_mins(tin))
                with c2:
                    tout = st.time_input("Time Out", mins_to_time(task.timeEnd), key=f"to_{task_key}_{day}_{id(task)}", 
                                        label_visibility="collapsed")
                    task.setValue("timeEnd", time_to_mins(tout))
                
                dur = task.taskDuration
                st.markdown(f"**DURATION: {dur//60}h {dur%60}m**")
                
                st.divider()
                
                # Notes
                st.markdown('<div class="label-text">NOTES</div>', unsafe_allow_html=True)
                st.session_state.task_notes[task_key] = st.text_area(
                    "notes", st.session_state.task_notes[task_key], height=100,
                    key=f"nt_{task_key}_{day}_{id(task)}", label_visibility="collapsed",
                    placeholder="Notes, links, details..."
                )
            
            # Tab 2: Subtasks
            with settings_tabs[1]:
                st.markdown('<div class="label-text">SUBTASKS</div>', unsafe_allow_html=True)
                st.progress(task.getProgress() / 100)
                
                to_remove = []
                for i, sub in enumerate(task.subTasks):
                    c1, c2, c3 = st.columns([1, 7, 1])
                    with c1:
                        done = st.checkbox("c", sub.status, key=f"sd_{task_key}_{day}_{i}_{id(task)}", 
                                         label_visibility="collapsed")
                        if done != sub.status:
                            sub.markDone() if done else sub.markUndone()
                    with c2:
                        new = st.text_input("t", sub.name, key=f"st_{task_key}_{day}_{i}_{id(task)}", 
                                          label_visibility="collapsed")
                        if new != sub.name:
                            sub.name = new
                    with c3:
                        if st.button("×", key=f"ds_{task_key}_{day}_{i}_{id(task)}"):
                            to_remove.append(sub)
                
                for sub in to_remove:
                    task.removeSubTask(sub)
                
                if st.button("+ SUBTASK", key=f"as_{task_key}_{day}_{id(task)}", use_container_width=True):
                    task.addSubTask(subTask("New", False))
                    st.rerun()
            
            # Tab 3: Task Config
            with settings_tabs[2]:
                st.markdown('<div class="label-text">TASK CONFIG</div>', unsafe_allow_html=True)
                
                # Difficulty
                c1, c2 = st.columns([3, 1])
                with c1:
                    diff = st.slider("Difficulty", 1, 5, task.taskDifficulty, key=f"df_{task_key}_{day}_{id(task)}")
                    task.setValue("taskDifficulty", diff)
                with c2:
                    st.markdown(f"### {'⭐' * diff}")
                
                # Event type
                event = st.selectbox(
                    "Type", ['Event', 'Assignment', 'Task', 'Chore'],
                    index=['Event', 'Assignment', 'Task', 'Chore'].index(EVENT_TAGS.get(task.eventTag, "Task")),
                    key=f"et_{task_key}_{day}_{id(task)}"
                )
                task.setValue("eventTag", EVENT_TAGS_REVERSE[event])
                
                # Time frame
                frame = st.selectbox(
                    "Time Frame", ['Day', 'Afternoon', 'Evening', 'All Day'],
                    index=['Day', 'Afternoon', 'Evening', 'All Day'].index(TIME_FRAMES.get(task.timeFrame, "Day")),
                    key=f"tf_{task_key}_{day}_{id(task)}"
                )
                task.setValue("timeFrame", TIME_FRAMES_REVERSE[frame])
                
                # Priority display
                st.metric("Priority", f"{task.priority}%")
    
    st.divider()
    
    # Action buttons (outside all tabs - affect all instances)
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("Save", key=f"save_{task_key}", use_container_width=True):
            st.session_state.week_instance.organizeWeek()
            # Save to JSON
            fn.save_tasks(st.session_state.week_instance)
            fn.save_notes(st.session_state.task_notes)
            fn.save_recurrences(st.session_state.task_recurrences)
            st.success("Saved to database!")
    with c2:
        if st.button("Cancel", key=f"cancel_{task_key}", use_container_width=True):
            st.session_state.selected_task = None
            st.rerun()
    with c3:
        if st.button("Delete All", key=f"del_{task_key}", use_container_width=True):
            delete_task(task_key)
            st.session_state.selected_task = None
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
    
    st.divider()
    st.markdown("**Data**")
    
    # Manual save button
    if st.button("💾 Save All", use_container_width=True):
        fn.save_tasks(st.session_state.week_instance)
        fn.save_notes(st.session_state.task_notes)
        fn.save_recurrences(st.session_state.task_recurrences)
        fn.save_shortcuts(st.session_state.shortcuts)
        fn.save_handbook_notes(st.session_state.handbook_notes)
        st.success("Saved!")
    
    # Export button
    if st.button("📄 Export", use_container_width=True):
        export_text = fn.export_to_text()
        st.download_button(
            label="Download .txt",
            data=export_text,
            file_name=f"bareminimum_export_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain",
            key="download_export"
        )
    
    # Backup button
    if st.button("🔄 Backup", use_container_width=True):
        backup_dir = fn.create_backup()
        st.success(f"Backup created!")
    
    # Auto-save toggle
    auto_save = st.checkbox("Auto-save", value=st.session_state.auto_save, key="auto_save_toggle")
    if auto_save != st.session_state.auto_save:
        st.session_state.auto_save = auto_save

# Main views
if st.session_state.current_view == 'planner':
    # Two-column layout: Task list | Task detail
    col_list, col_detail = st.columns([1, 1])
    
    with col_list:
        # Week tabs at top
        days = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
        days_full = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        tabs = st.tabs(days)
        
        for i, (day_short, day_full) in enumerate(zip(days, days_full)):
            day_obj = st.session_state.week_instance.days[i]
            
            with tabs[i]:
                # Sort by selector (compact)
                st.markdown('<div class="label-text">> Sort By</div>', unsafe_allow_html=True)
                
                # Priority sections
                if day_obj.highPriority:
                    st.markdown("**High Priority**")
                    for task in day_obj.highPriority:
                        render_task_item(task, day_obj, day_full)
                
                if day_obj.mediumPriority:
                    st.markdown("**Medium Priority**")
                    for task in day_obj.mediumPriority:
                        render_task_item(task, day_obj, day_full)
                
                if day_obj.smallPriority:
                    st.markdown("**Low Priority**")
                    for task in day_obj.smallPriority:
                        render_task_item(task, day_obj, day_full)
                
                if not day_obj.tasks:
                    st.info("No tasks")
                
                st.divider()
                if st.button(f"+ ADD TO {day_short}", key=f"add_{day_full}", use_container_width=True):
                    add_new_task(day_obj)
                    st.rerun()
    
    with col_detail:
        # Show selected task detail
        if st.session_state.selected_task:
            # Find the selected task
            selected_task = None
            selected_day_obj = None
            
            for day in st.session_state.week_instance.days:
                for task in day.tasks:
                    if get_task_key(task) == st.session_state.selected_task:
                        selected_task = task
                        selected_day_obj = day
                        break
                if selected_task:
                    break
            
            if selected_task:
                render_task_detail(selected_task, selected_day_obj)
            else:
                st.info("Select a task to view details")
        else:
            st.info("Select a task to view details")

elif st.session_state.current_view == 'handbook':
    handbook_tabs = st.tabs(["SHORTCUTS", "REMINDERS"])
    
    with handbook_tabs[0]:
        st.markdown('<div class="label-text">DOCS</div>', unsafe_allow_html=True)
        
        # Display existing shortcuts
        to_delete = None
        for idx, shortcut in enumerate(st.session_state.shortcuts):
            c1, c2, c3 = st.columns([3, 1, 1])
            with c1:
                st.text(shortcut["name"])
            with c2:
                if st.button("Link", key=f"link_{idx}", use_container_width=True):
                    st.markdown(f"[Open {shortcut['name']}]({shortcut['url']})")
            with c3:
                if st.button("Delete", key=f"del_shortcut_{idx}", use_container_width=True):
                    to_delete = idx
        
        # Delete shortcut if requested
        if to_delete is not None:
            fn.delete_shortcut(to_delete)
            st.session_state.shortcuts = fn.load_shortcuts()
            st.rerun()
        
        st.divider()
        
        # Add new shortcut
        with st.expander("+ Add Shortcut", expanded=False):
            new_name = st.text_input("Name", key="new_shortcut_name")
            new_url = st.text_input("URL", key="new_shortcut_url")
            if st.button("Add", key="add_shortcut_btn"):
                if new_name and new_url:
                    fn.add_shortcut(new_name, new_url)
                    st.session_state.shortcuts = fn.load_shortcuts()
                    st.rerun()
    
    with handbook_tabs[1]:
        st.markdown('<div class="label-text">NOTEPAD</div>', unsafe_allow_html=True)
        notes = st.text_area("", height=400, value=st.session_state.handbook_notes, 
                            placeholder="Notes...", key="notepad", label_visibility="collapsed")
        
        # Save notes if changed
        if notes != st.session_state.handbook_notes:
            st.session_state.handbook_notes = notes
            fn.save_handbook_notes(notes)

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
