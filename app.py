import streamlit as st
import pandas as pd
from datetime import date, time, datetime, timedelta
import sys
sys.path.append('.')

# Import the data structures
from dataStruct import Task, subTask, Bundle, Day, week

st.set_page_config(page_title="Recurring Task Scheduler", layout="wide")

st.title("📅 Recurring Task Scheduler")

# Mapping for display
DIFFICULTY_MAP = {1: "Very Easy", 2: "Easy", 3: "Average", 4: "Hard", 5: "Very Hard"}
EVENT_TAGS = {5: "Event", 4: "Assignment", 3: "Task", 1: "Chore"}
EVENT_TAGS_REVERSE = {v: k for k, v in EVENT_TAGS.items()}
TIME_FRAMES = {1: "Day", 2: "Afternoon", 3: "Evening", 4: "All Day"}
TIME_FRAMES_REVERSE = {v: k for k, v in TIME_FRAMES.items()}
DEADLINE_TYPES = {1: "Hard", 0: "Soft"}

# Initialize session state
if 'week_instance' not in st.session_state:
    st.session_state.week_instance = week()
    
    # Create sample task
    sample_task = Task()
    sample_task.setValue("taskName", "Computer Programming Terminal App")
    sample_task.setValue("taskDifficulty", 4)
    sample_task.setValue("taskDeadline", 1)  # Hard deadline
    sample_task.setValue("timeStart", 540)  # 9:00 AM (in minutes)
    sample_task.setValue("timeEnd", 1020)  # 5:00 PM (in minutes)
    sample_task.setValue("eventTag", 4)  # Assignment
    sample_task.setValue("timeFrame", 4)  # All Day
    sample_task.setValue("day", "Monday")
    
    # Add subtasks
    sample_task.addSubTask(subTask("Plan the Task", False))
    sample_task.addSubTask(subTask("Revise the Plan", False))
    sample_task.addSubTask(subTask("Code the App", False))
    sample_task.addSubTask(subTask("Check and Revise", False))
    
    sample_task.setPriority()
    
    # Add task to Monday
    st.session_state.week_instance.Monday.addTask(sample_task)
    st.session_state.week_instance.organizeWeek()

if 'bundles' not in st.session_state:
    st.session_state.bundles = []

if 'task_notes' not in st.session_state:
    # Store notes separately since Task class doesn't have notes attribute
    st.session_state.task_notes = {}

# ---------- Helper Functions ----------
def minutes_to_time(minutes):
    """Convert minutes to time object"""
    hours = minutes // 60
    mins = minutes % 60
    return time(hours, mins)

def time_to_minutes(t):
    """Convert time object to minutes"""
    return t.hour * 60 + t.minute

def calculate_duration_display(task):
    """Display duration in human readable format"""
    duration = task.taskDuration
    hours = duration // 60
    mins = duration % 60
    if hours > 0:
        return f"{hours}h {mins}m"
    else:
        return f"{mins}m"

def get_task_id(task):
    """Generate unique ID for task based on object id"""
    return id(task)

def add_new_task_to_day(day_obj):
    """Add a new task to a specific day"""
    new_task = Task()
    new_task.setValue("taskName", "New Task")
    new_task.setValue("day", day_obj.name)
    new_task.addSubTask(subTask("New subtask", False))
    new_task.setPriority()
    day_obj.addTask(new_task)
    st.session_state.week_instance.organizeWeek()

def delete_task_from_day(day_obj, task):
    """Delete a task from a day"""
    day_obj.removeTask(task)
    st.session_state.week_instance.organizeWeek()

def create_bundle_from_task(task):
    """Create a bundle from a task for multi-day recurrence"""
    bundle = Bundle()
    bundle.addTask(task)
    return bundle

# ---------- Task Renderer ----------
def render_task(task, day_obj, current_day):
    """Renders a single task with all its features"""
    task_id = get_task_id(task)
    
    # Get or initialize notes for this task
    if task_id not in st.session_state.task_notes:
        st.session_state.task_notes[task_id] = ""
    
    with st.expander(f"📋 {task.taskName}", expanded=False):
        
        # ============ BASICS SECTION ============
        st.markdown("### 📝 Basics")
        
        # Task name
        new_name = st.text_input(
            "Task Name",
            value=task.taskName,
            key=f"name_{task_id}_{current_day}"
        )
        if new_name != task.taskName:
            task.setValue("taskName", new_name)
        
        # Deadline type
        col1, col2 = st.columns(2)
        with col1:
            hard_checked = task.taskDeadline == 1
            if st.checkbox("☑️ Hard Deadline", value=hard_checked, key=f"hard_{task_id}_{current_day}"):
                task.setValue("taskDeadline", 1)
            else:
                task.setValue("taskDeadline", 0)
        
        with col2:
            soft_checked = task.taskDeadline == 0
            st.markdown(f"**Current:** {'Hard' if task.taskDeadline == 1 else 'Soft'}")
        
        # Time In and Time Out
        col1, col2, col3 = st.columns([2, 2, 2])
        with col1:
            time_in = st.time_input(
                "⏰ Time In",
                value=minutes_to_time(task.timeStart),
                key=f"time_in_{task_id}_{current_day}"
            )
            new_time_in = time_to_minutes(time_in)
            if new_time_in != task.timeStart:
                task.setValue("timeStart", new_time_in)
        
        with col2:
            time_out = st.time_input(
                "⏰ Time Out",
                value=minutes_to_time(task.timeEnd),
                key=f"time_out_{task_id}_{current_day}"
            )
            new_time_out = time_to_minutes(time_out)
            if new_time_out != task.timeEnd:
                task.setValue("timeEnd", new_time_out)
        
        with col3:
            duration_display = calculate_duration_display(task)
            st.metric("Duration", duration_display)
            st.caption(f"Category: {task.durationCategory}")
        
        st.divider()
        
        # ============ SUB-TASKS SECTION ============
        st.markdown("### ✅ Sub-tasks")
        
        # Show progress
        progress = task.getProgress()
        st.progress(progress / 100, text=f"Progress: {progress}%")
        
        # Render existing subtasks
        subtasks_to_remove = []
        for sub_idx, subtask in enumerate(task.subTasks):
            col1, col2, col3 = st.columns([1, 5, 1])
            
            with col1:
                new_status = st.checkbox(
                    "Done",
                    value=subtask.status,
                    key=f"subtask_done_{task_id}_{current_day}_{sub_idx}",
                    label_visibility="collapsed"
                )
                if new_status != subtask.status:
                    if new_status:
                        subtask.markDone()
                    else:
                        subtask.markUndone()
            
            with col2:
                new_text = st.text_input(
                    "Subtask",
                    value=subtask.name,
                    key=f"subtask_text_{task_id}_{current_day}_{sub_idx}",
                    label_visibility="collapsed"
                )
                if new_text != subtask.name:
                    subtask.name = new_text
            
            with col3:
                if st.button("🗑️", key=f"del_subtask_{task_id}_{current_day}_{sub_idx}"):
                    subtasks_to_remove.append(subtask)
        
        # Remove marked subtasks
        for subtask in subtasks_to_remove:
            task.removeSubTask(subtask)
        
        # Add new subtask button
        if st.button("➕ Add Subtask", key=f"add_subtask_{task_id}_{current_day}"):
            task.addSubTask(subTask("New subtask", False))
            st.rerun()
        
        st.divider()
        
        # ============ NOTES SECTION ============
        st.markdown("### 📓 Notes")
        notes = st.text_area(
            "Notes, details, and links",
            value=st.session_state.task_notes[task_id],
            height=150,
            key=f"notes_{task_id}_{current_day}",
            placeholder="Add notes, details, links, or reminders here..."
        )
        st.session_state.task_notes[task_id] = notes
        
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
                value=task.taskDifficulty,
                key=f"difficulty_{task_id}_{current_day}"
            )
            if difficulty != task.taskDifficulty:
                task.setValue("taskDifficulty", difficulty)
        
        with col2:
            st.markdown(f"### {'⭐' * difficulty}")
            st.caption(DIFFICULTY_MAP[difficulty])
        
        # Event Type
        current_event_type = EVENT_TAGS.get(task.eventTag, "Task")
        event_type = st.selectbox(
            "Event Type",
            ['Event', 'Assignment', 'Task', 'Chore'],
            index=['Event', 'Assignment', 'Task', 'Chore'].index(current_event_type),
            key=f"event_type_{task_id}_{current_day}"
        )
        new_event_tag = EVENT_TAGS_REVERSE[event_type]
        if new_event_tag != task.eventTag:
            task.setValue("eventTag", new_event_tag)
        
        # Time Frame
        current_time_frame = TIME_FRAMES.get(task.timeFrame, "Day")
        time_frame = st.selectbox(
            "Time Frame",
            ['Day', 'Afternoon', 'Evening', 'All Day'],
            index=['Day', 'Afternoon', 'Evening', 'All Day'].index(current_time_frame),
            key=f"time_frame_{task_id}_{current_day}"
        )
        new_time_frame = TIME_FRAMES_REVERSE[time_frame]
        if new_time_frame != task.timeFrame:
            task.setValue("timeFrame", new_time_frame)
        
        # Priority Display
        st.metric("Calculated Priority", f"{task.priority}%")
        
        st.divider()
        
        # Delete entire task button
        if st.button(f"🗑️ Delete Task: {task.taskName}", key=f"del_task_{task_id}_{current_day}", type="secondary"):
            delete_task_from_day(day_obj, task)
            st.rerun()

# ---------- Top Bar - Add New Task ----------
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("### Manage Your Weekly Tasks")
with col2:
    if st.button("➕ Add New Task", type="primary", key="add_task_btn"):
        # Add to Monday by default
        add_new_task_to_day(st.session_state.week_instance.Monday)
        st.rerun()

st.divider()

# ---------- Render Week Tabs ----------
week_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
week_tabs = st.tabs(week_days)

for i, day_name in enumerate(week_days):
    day_obj = st.session_state.week_instance.days[i]
    
    with week_tabs[i]:
        st.header(f"📅 {day_name}")
        
        # Add task button for this specific day
        if st.button(f"➕ Add Task to {day_name}", key=f"add_task_{day_name}"):
            add_new_task_to_day(day_obj)
            st.rerun()
        
        st.divider()
        
        if not day_obj.tasks:
            st.info("✨ No tasks scheduled for this day")
        else:
            # Show priority categories
            if day_obj.highPriority:
                st.markdown("#### 🔴 High Priority Tasks")
                for task in day_obj.highPriority:
                    render_task(task, day_obj, day_name)
                    st.markdown("---")
            
            if day_obj.mediumPriority:
                st.markdown("#### 🟡 Medium Priority Tasks")
                for task in day_obj.mediumPriority:
                    render_task(task, day_obj, day_name)
                    st.markdown("---")
            
            if day_obj.smallPriority:
                st.markdown("#### 🟢 Low Priority Tasks")
                for task in day_obj.smallPriority:
                    render_task(task, day_obj, day_name)
                    st.markdown("---")

# ---------- Summary Statistics ----------
st.divider()
st.markdown("### 📊 Weekly Overview")

# Calculate statistics
total_tasks = sum(len(day.tasks) for day in st.session_state.week_instance.days)
total_subtasks = sum(len(task.subTasks) for day in st.session_state.week_instance.days for task in day.tasks)
completed_subtasks = sum(
    sum(1 for sub in task.subTasks if sub.status) 
    for day in st.session_state.week_instance.days 
    for task in day.tasks
)
avg_difficulty = sum(task.taskDifficulty for day in st.session_state.week_instance.days for task in day.tasks) / total_tasks if total_tasks > 0 else 0

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Tasks", total_tasks)

with col2:
    st.metric("Total Subtasks", total_subtasks)

with col3:
    st.metric("Completed Subtasks", f"{completed_subtasks}/{total_subtasks}")

with col4:
    st.metric("Avg Difficulty", f"{'⭐' * int(avg_difficulty)}")

# Show breakdown by event type
st.markdown("#### Task Distribution by Type")
col1, col2, col3, col4 = st.columns(4)

events = sum(len(day.Event) for day in st.session_state.week_instance.days)
assignments = sum(len(day.Assignment) for day in st.session_state.week_instance.days)
tasks = sum(len(day.Tasks) for day in st.session_state.week_instance.days)
chores = sum(len(day.Chores) for day in st.session_state.week_instance.days)

with col1:
    st.metric("Events", events)
with col2:
    st.metric("Assignments", assignments)
with col3:
    st.metric("Tasks", tasks)
with col4:
    st.metric("Chores", chores)
