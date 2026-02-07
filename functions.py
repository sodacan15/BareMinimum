import json
import os
from datetime import datetime
from dataStruct import Task, subTask, week, Day

# File paths
TASKS_JSON = "data/tasks.json"
LINKS_JSON = "data/links.json"
SETTINGS_JSON = "data/settings.json"

# Ensure data directory exists
os.makedirs("data", exist_ok=True)

# ==================== JSON OPERATIONS ====================

def load_json(filepath, default=None):
    """Load JSON file, return default if file doesn't exist"""
    if default is None:
        default = {}
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                return json.load(f)
        return default
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return default

def save_json(filepath, data):
    """Save data to JSON file"""
    try:
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving {filepath}: {e}")
        return False

# ==================== TASK OPERATIONS ====================

def save_tasks(week_instance):
    """Save all tasks from week instance to JSON"""
    tasks_data = []
    
    for day in week_instance.days:
        for task in day.tasks:
            task_dict = {
                "taskName": task.taskName,
                "taskDifficulty": task.taskDifficulty,
                "taskDeadline": task.taskDeadline,
                "timeStart": task.timeStart,
                "timeEnd": task.timeEnd,
                "eventTag": task.eventTag,
                "timeFrame": task.timeFrame,
                "day": day.name,
                "subTasks": [
                    {"name": sub.name, "status": sub.status}
                    for sub in task.subTasks
                ],
                "notes": ""  # Will be stored separately in session
            }
            tasks_data.append(task_dict)
    
    return save_json(TASKS_JSON, tasks_data)

def load_tasks():
    """Load tasks from JSON and return week instance"""
    tasks_data = load_json(TASKS_JSON, default=[])
    week_instance = week()
    
    for task_dict in tasks_data:
        task = Task()
        task.setValue("taskName", task_dict.get("taskName", "Task"))
        task.setValue("taskDifficulty", task_dict.get("taskDifficulty", 3))
        task.setValue("taskDeadline", task_dict.get("taskDeadline", 1))
        task.setValue("timeStart", task_dict.get("timeStart", 0))
        task.setValue("timeEnd", task_dict.get("timeEnd", 0))
        task.setValue("eventTag", task_dict.get("eventTag", 3))
        task.setValue("timeFrame", task_dict.get("timeFrame", 2))
        task.setValue("day", task_dict.get("day", "Monday"))
        
        # Add subtasks
        for sub_dict in task_dict.get("subTasks", []):
            task.addSubTask(subTask(sub_dict.get("name", "Subtask"), sub_dict.get("status", False)))
        
        task.setPriority()
        
        # Add to appropriate day
        day_name = task_dict.get("day", "Monday")
        week_instance.addTaskToDay(task, day_name)
    
    week_instance.organizeWeek()
    return week_instance

def add_task_to_json(task_dict):
    """Add a new task to JSON storage"""
    tasks_data = load_json(TASKS_JSON, default=[])
    tasks_data.append(task_dict)
    return save_json(TASKS_JSON, tasks_data)

def delete_task_from_json(task_name):
    """Delete a task from JSON storage by name"""
    tasks_data = load_json(TASKS_JSON, default=[])
    tasks_data = [t for t in tasks_data if t.get("taskName") != task_name]
    return save_json(TASKS_JSON, tasks_data)

def update_task_in_json(task_name, updated_task_dict):
    """Update a task in JSON storage"""
    tasks_data = load_json(TASKS_JSON, default=[])
    for i, task in enumerate(tasks_data):
        if task.get("taskName") == task_name:
            tasks_data[i] = updated_task_dict
            break
    return save_json(TASKS_JSON, tasks_data)

# ==================== LINK/SHORTCUT OPERATIONS ====================

def load_shortcuts():
    """Load shortcuts from JSON"""
    return load_json(LINKS_JSON, default=[
        {"name": "Google Drive", "url": "https://drive.google.com"},
        {"name": "Gmail", "url": "https://gmail.com"}
    ])

def save_shortcuts(shortcuts):
    """Save shortcuts to JSON"""
    return save_json(LINKS_JSON, shortcuts)

def add_shortcut(name, url):
    """Add a new shortcut"""
    shortcuts = load_shortcuts()
    shortcuts.append({"name": name, "url": url})
    return save_shortcuts(shortcuts)

def delete_shortcut(index):
    """Delete a shortcut by index"""
    shortcuts = load_shortcuts()
    if 0 <= index < len(shortcuts):
        shortcuts.pop(index)
        return save_shortcuts(shortcuts)
    return False

def update_shortcut(index, name, url):
    """Update a shortcut by index"""
    shortcuts = load_shortcuts()
    if 0 <= index < len(shortcuts):
        shortcuts[index] = {"name": name, "url": url}
        return save_shortcuts(shortcuts)
    return False

# ==================== NOTES OPERATIONS ====================

def save_notes(task_notes):
    """Save task notes to JSON"""
    notes_data = {
        "task_notes": task_notes,
        "last_updated": datetime.now().isoformat()
    }
    return save_json("data/notes.json", notes_data)

def load_notes():
    """Load task notes from JSON"""
    notes_data = load_json("data/notes.json", default={"task_notes": {}})
    return notes_data.get("task_notes", {})

# ==================== SETTINGS OPERATIONS ====================

def save_settings(settings):
    """Save app settings"""
    return save_json(SETTINGS_JSON, settings)

def load_settings():
    """Load app settings"""
    return load_json(SETTINGS_JSON, default={
        "theme": "dark",
        "default_view": "planner",
        "auto_save": True
    })

# ==================== RECURRENCE OPERATIONS ====================

def save_recurrences(recurrences):
    """Save task recurrences to JSON"""
    return save_json("data/recurrences.json", recurrences)

def load_recurrences():
    """Load task recurrences from JSON"""
    return load_json("data/recurrences.json", default={})

# ==================== HANDBOOK OPERATIONS ====================

def save_handbook_notes(notes):
    """Save handbook notepad content"""
    return save_json("data/handbook_notes.json", {"notes": notes, "last_updated": datetime.now().isoformat()})

def load_handbook_notes():
    """Load handbook notepad content"""
    data = load_json("data/handbook_notes.json", default={"notes": ""})
    return data.get("notes", "")

# ==================== BACKUP OPERATIONS ====================

def create_backup():
    """Create backup of all data"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = f"data/backups/{timestamp}"
    os.makedirs(backup_dir, exist_ok=True)
    
    # Copy all JSON files to backup
    files_to_backup = [
        TASKS_JSON,
        LINKS_JSON,
        SETTINGS_JSON,
        "data/notes.json",
        "data/recurrences.json",
        "data/handbook_notes.json"
    ]
    
    for filepath in files_to_backup:
        if os.path.exists(filepath):
            data = load_json(filepath)
            filename = os.path.basename(filepath)
            save_json(f"{backup_dir}/{filename}", data)
    
    return backup_dir

def list_backups():
    """List all available backups"""
    backup_dir = "data/backups"
    if os.path.exists(backup_dir):
        return sorted(os.listdir(backup_dir), reverse=True)
    return []

def restore_backup(backup_name):
    """Restore from a backup"""
    backup_dir = f"data/backups/{backup_name}"
    if not os.path.exists(backup_dir):
        return False
    
    files_to_restore = os.listdir(backup_dir)
    for filename in files_to_restore:
        backup_file = f"{backup_dir}/{filename}"
        target_file = f"data/{filename}"
        data = load_json(backup_file)
        save_json(target_file, data)
    
    return True

# ==================== UTILITY FUNCTIONS ====================

def clear_all_data():
    """Clear all data (use with caution)"""
    save_json(TASKS_JSON, [])
    save_json(LINKS_JSON, [])
    save_json("data/notes.json", {"task_notes": {}})
    save_json("data/recurrences.json", {})
    save_json("data/handbook_notes.json", {"notes": ""})
    return True

def get_statistics():
    """Get statistics about tasks"""
    tasks_data = load_json(TASKS_JSON, default=[])
    
    total_tasks = len(tasks_data)
    total_subtasks = sum(len(t.get("subTasks", [])) for t in tasks_data)
    completed_subtasks = sum(
        sum(1 for sub in t.get("subTasks", []) if sub.get("status", False))
        for t in tasks_data
    )
    
    tasks_by_day = {}
    for task in tasks_data:
        day = task.get("day", "Unknown")
        tasks_by_day[day] = tasks_by_day.get(day, 0) + 1
    
    return {
        "total_tasks": total_tasks,
        "total_subtasks": total_subtasks,
        "completed_subtasks": completed_subtasks,
        "completion_rate": round((completed_subtasks / total_subtasks * 100) if total_subtasks > 0 else 0, 1),
        "tasks_by_day": tasks_by_day
    }

def export_to_text():
    """Export all tasks to a readable text format"""
    tasks_data = load_json(TASKS_JSON, default=[])
    output = []
    output.append("=== BAREMINIMUM TASK EXPORT ===")
    output.append(f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    output.append("")
    
    days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    for day in days_order:
        day_tasks = [t for t in tasks_data if t.get("day") == day]
        if day_tasks:
            output.append(f"\n{'='*50}")
            output.append(f"{day.upper()}")
            output.append('='*50)
            
            for task in day_tasks:
                output.append(f"\n• {task.get('taskName', 'Unnamed')}")
                output.append(f"  Difficulty: {task.get('taskDifficulty', 0)}/5")
                output.append(f"  Time: {task.get('timeStart', 0)//60:02d}:{task.get('timeStart', 0)%60:02d} - {task.get('timeEnd', 0)//60:02d}:{task.get('timeEnd', 0)%60:02d}")
                
                subtasks = task.get("subTasks", [])
                if subtasks:
                    output.append("  Subtasks:")
                    for sub in subtasks:
                        status = "✓" if sub.get("status", False) else "○"
                        output.append(f"    {status} {sub.get('name', '')}")
    
    return "\n".join(output)
