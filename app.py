import streamlit as st
from datetime import time
import sys
sys.path.append('.')

# Import the data structures
from dataStruct import Task, subTask, week

st.set_page_config(page_title="Task Scheduler", layout="wide")

st.title("📅 Task Scheduler")

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
    
    with st.expander(f"📋 {task.taskName}", expanded=False):
        
        # RECURRENCE SECTION
        st.markdown("#### 🔄 Recurrence")
        
        all_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        available_days = [d for d in all_days if d not in recurrence_days]
        
        if available_days and len(recurrence_days) < 7:
            c1, c2 = st.columns([4, 1])
            with c1:
                new_day = st.selectbox(
                    "Add day",
                    ['...'] + available_days,
                    key=f"add_{task_key}_{current_day}",
                    label_visibility="collapsed"
                )
            with c2:
                if st.button("➕", key=f"btn_{task_key}_{current_day}"):
                    if new_day != '...':
                        add_recurrence(task_key, new_day)
                        st.rerun()
        
        st.divider()
        
        # RECURRENCE TABS
        if len(recurrence_days) > 1:
            tabs = st.tabs([f"{d} ❌" for d in recurrence_days])
        else:
            tabs = st.tabs(recurrence_days)
        
        for idx, day in enumerate(recurrence_days):
            with tabs[idx]:
                if len(recurrence_days) > 1:
                    if st.button(f"❌ Remove {day}", key=f"rm_{task_key}_{day}_{current_day}"):
                        remove_recurrence(task_key, day)
                        st.rerun()
                    st.divider()
                
                # BASICS
                st.markdown("**📝 Basics**")
                
                task.setValue("taskName", st.text_input(
                    "Name", task.taskName, key=f"n_{task_key}_{day}_{current_day}"
                ))
                
                c1, c2 = st.columns(2)
                with c1:
                    hard = st.checkbox("Hard", task.taskDeadline == 1, key=f"h_{task_key}_{day}_{current_day}")
                    task.setValue("taskDeadline", 1 if hard else 0)
                with c2:
                    st.checkbox("Soft", task.taskDeadline == 0, key=f"s_{task_key}_{day}_{current_day}", disabled=True)
                
                # TIME
                c1, c2, c3 = st.columns(3)
                with c1:
                    tin = st.time_input("In", mins_to_time(task.timeStart), key=f"ti_{task_key}_{day}_{current_day}")
                    task.setValue("timeStart", time_to_mins(tin))
                with c2:
                    tout = st.time_input("Out", mins_to_time(task.timeEnd), key=f"to_{task_key}_{day}_{current_day}")
                    task.setValue("timeEnd", time_to_mins(tout))
                with c3:
                    dur = task.taskDuration
                    st.metric("Duration", f"{dur//60}h {dur%60}m")
                
                st.divider()
                
                # SUBTASKS
                st.markdown("**✅ Subtasks**")
                st.progress(task.getProgress() / 100)
                
                to_remove = []
                for i, sub in enumerate(task.subTasks):
                    c1, c2, c3 = st.columns([1, 6, 1])
                    with c1:
                        done = st.checkbox("", sub.status, key=f"sd_{task_key}_{day}_{current_day}_{i}", label_visibility="collapsed")
                        if done != sub.status:
                            sub.markDone() if done else sub.markUndone()
                    with c2:
                        new = st.text_input("", sub.name, key=f"st_{task_key}_{day}_{current_day}_{i}", label_visibility="collapsed")
                        if new != sub.name:
                            sub.name = new
                    with c3:
                        if st.button("🗑", key=f"ds_{task_key}_{day}_{current_day}_{i}"):
                            to_remove.append(sub)
                
                for sub in to_remove:
                    task.removeSubTask(sub)
                
                if st.button("➕ Subtask", key=f"as_{task_key}_{day}_{current_day}"):
                    task.addSubTask(subTask("New", False))
                    st.rerun()
                
                st.divider()
                
                # NOTES
                st.markdown("**📓 Notes**")
                st.session_state.task_notes[task_key] = st.text_area(
                    "", st.session_state.task_notes[task_key], height=100,
                    key=f"nt_{task_key}_{day}_{current_day}", label_visibility="collapsed",
                    placeholder="Notes, links, details..."
                )
                
                st.divider()
                
                # SETTINGS
                st.markdown("**⚙️ Settings**")
                
                c1, c2 = st.columns([3, 1])
                with c1:
                    diff = st.slider("Difficulty", 1, 5, task.taskDifficulty, key=f"df_{task_key}_{day}_{current_day}")
                    task.setValue("taskDifficulty", diff)
                with c2:
                    st.markdown(f"### {'⭐' * diff}")
                
                event = st.selectbox(
                    "Type", ['Event', 'Assignment', 'Task', 'Chore'],
                    index=['Event', 'Assignment', 'Task', 'Chore'].index(EVENT_TAGS.get(task.eventTag, "Task")),
                    key=f"et_{task_key}_{day}_{current_day}"
                )
                task.setValue("eventTag", EVENT_TAGS_REVERSE[event])
                
                frame = st.selectbox(
                    "Frame", ['Day', 'Afternoon', 'Evening', 'All Day'],
                    index=['Day', 'Afternoon', 'Evening', 'All Day'].index(TIME_FRAMES.get(task.timeFrame, "Day")),
                    key=f"tf_{task_key}_{day}_{current_day}"
                )
                task.setValue("timeFrame", TIME_FRAMES_REVERSE[frame])
                
                st.metric("Priority", f"{task.priority}%")
        
        st.divider()
        if st.button(f"🗑 Delete All", key=f"del_{task_key}_{current_day}"):
            delete_task(task_key)
            st.rerun()

# ---------- UI ----------
c1, c2 = st.columns([4, 1])
with c2:
    if st.button("➕ New Task", type="primary"):
        add_new_task(st.session_state.week_instance.Monday)
        st.rerun()

st.divider()

# WEEK TABS
days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
tabs = st.tabs(days)

for i, day_name in enumerate(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']):
    day_obj = st.session_state.week_instance.days[i]
    
    with tabs[i]:
        if st.button(f"➕ Add to {days[i]}", key=f"add_{day_name}"):
            add_new_task(day_obj)
            st.rerun()
        
        if not day_obj.tasks:
            st.info("No tasks")
        else:
            if day_obj.highPriority:
                st.markdown("**🔴 High**")
                for task in day_obj.highPriority:
                    render_task(task, day_obj, day_name)
            
            if day_obj.mediumPriority:
                st.markdown("**🟡 Medium**")
                for task in day_obj.mediumPriority:
                    render_task(task, day_obj, day_name)
            
            if day_obj.smallPriority:
                st.markdown("**🟢 Low**")
                for task in day_obj.smallPriority:
                    render_task(task, day_obj, day_name)

# STATS
st.divider()
st.markdown("### 📊 Overview")

total = sum(len(d.tasks) for d in st.session_state.week_instance.days)
subs = sum(len(t.subTasks) for d in st.session_state.week_instance.days for t in d.tasks)
done = sum(sum(1 for s in t.subTasks if s.status) for d in st.session_state.week_instance.days for t in d.tasks)

c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Tasks", total)
with c2:
    st.metric("Subtasks", subs)
with c3:
    st.metric("Done", f"{done}/{subs}")
