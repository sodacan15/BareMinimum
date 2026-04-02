import json
import os
import uuid
from datetime import datetime
from supabase import create_client, Client
from dataStruct import Task, subTask, week, Day

def _init_supabase():
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_SERVICE_KEY")
    if url and key:
        return create_client(url, key)
    return None

supabase: Client = _init_supabase()

LINKS_JSON = "links.json"
SETTINGS_JSON = "settings.json"

os.makedirs("data", exist_ok=True)

EVENT_TAG_TO_TYPE = {5: "Event", 4: "Assignment", 3: "Task", 1: "Chore"}
EVENT_TYPE_TO_TAG = {"Event": 5, "Assignment": 4, "Task": 3, "Chore": 1}

# ==================== JSON HELPERS (non-Supabase data) ====================

def load_json(filepath, default=None):
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
    try:
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving {filepath}: {e}")
        return False

# ==================== TIME HELPERS ====================

def mins_to_time_str(minutes):
    h = int(minutes) // 60
    m = int(minutes) % 60
    return f"{h:02d}:{m:02d}:00"

def time_str_to_mins(time_str):
    try:
        parts = str(time_str).split(":")
        return int(parts[0]) * 60 + int(parts[1])
    except Exception:
        return 0

# ==================== TASK OPERATIONS (Supabase) ====================

def save_tasks(week_instance):
    """Save all tasks to Supabase (Tasks + Recurrence + Subtasks)."""
    try:
        memory_tasks = {}
        memory_pairs = []

        for day in week_instance.days:
            for task in day.tasks:
                name = task.taskName
                if name not in memory_tasks:
                    memory_tasks[name] = task
                memory_pairs.append((name, day.name, task))

        existing_tasks = supabase.table("Tasks").select("TaskID, TaskName").execute().data
        existing_task_map = {t["TaskName"]: t["TaskID"] for t in existing_tasks}

        for task_name, task_id in list(existing_task_map.items()):
            if task_name not in memory_tasks:
                supabase.table("Recurrence").delete().eq("TaskID", task_id).execute()
                supabase.table("Tasks").delete().eq("TaskID", task_id).execute()
                del existing_task_map[task_name]

        task_id_map = {}
        for task_name, task in memory_tasks.items():
            row = {
                "TaskName": task_name,
                "DayCount": task.taskRecurrence,
                "TaskStatus": "active" if task.taskDeadline == 1 else "pending",
            }
            if task_name in existing_task_map:
                task_id = existing_task_map[task_name]
                supabase.table("Tasks").update(row).eq("TaskID", task_id).execute()
            else:
                result = supabase.table("Tasks").insert(row).execute()
                task_id = result.data[0]["TaskID"]
            task_id_map[task_name] = task_id

        existing_recs = supabase.table("Recurrence").select("RecurrenceID, TaskID, Day").execute().data
        existing_rec_map = {(r["TaskID"], r["Day"]): r["RecurrenceID"] for r in existing_recs}

        memory_rec_keys = set()
        for task_name, day_name, _ in memory_pairs:
            tid = task_id_map.get(task_name)
            if tid:
                memory_rec_keys.add((tid, day_name))

        for (tid, day), rec_id in list(existing_rec_map.items()):
            if (tid, day) not in memory_rec_keys:
                supabase.table("Recurrence").delete().eq("RecurrenceID", rec_id).execute()

        for task_name, day_name, task in memory_pairs:
            tid = task_id_map.get(task_name)
            if not tid:
                continue
            event_type = EVENT_TAG_TO_TYPE.get(task.eventTag, "Task")
            rec_row = {
                "TaskID": tid,
                "TimeIn": mins_to_time_str(task.timeStart),
                "TimeOut": mins_to_time_str(task.timeEnd),
                "Day": day_name,
                "Difficulty": task.taskDifficulty,
                "TaskType": event_type,
                "Priority": float(task.priority),
                "Classification": str(task.timeFrame),
                "RecurrenceStatus": "active",
            }
            key = (tid, day_name)
            if key in existing_rec_map:
                supabase.table("Recurrence").update(rec_row).eq("RecurrenceID", existing_rec_map[key]).execute()
            else:
                supabase.table("Recurrence").insert(rec_row).execute()

        for task_name, day_name, task in memory_pairs:
            tid = task_id_map.get(task_name)
            if not tid:
                continue
            supabase.table("Subtasks").delete().eq("TaskID", tid).eq("SubtaskDay", day_name).execute()
            for sub in task.subTasks:
                supabase.table("Subtasks").insert({
                    "TaskID": tid,
                    "SubtaskDay": day_name,
                    "Subtask": sub.name,
                    "TimeAllotment": 0,
                    "SubtaskStatus": "done" if sub.status else "pending",
                }).execute()

        return True
    except Exception as e:
        print(f"Error saving tasks to Supabase: {e}")
        return False

def load_tasks():
    """Load tasks from Supabase and return a week instance."""
    week_instance = week()
    try:
        result = supabase.table("Recurrence").select(
            "*, Tasks(TaskID, TaskName, DayCount, TaskStatus)"
        ).execute()

        subs_result = supabase.table("Subtasks").select("*").execute()
        subtasks_map = {}
        for s in subs_result.data:
            key = (s.get("TaskID"), s.get("SubtaskDay"))
            subtasks_map.setdefault(key, []).append(s)

        for rec in result.data:
            task_info = rec.get("Tasks") or {}
            if not task_info:
                continue

            task = Task()
            task.setValue("taskName", task_info.get("TaskName", "Task"))
            task.setValue("taskDifficulty", rec.get("Difficulty", 3))
            task.setValue("taskDeadline", 1 if task_info.get("TaskStatus") == "active" else 0)
            task.setValue("timeStart", time_str_to_mins(rec.get("TimeIn", "09:00:00")))
            task.setValue("timeEnd", time_str_to_mins(rec.get("TimeOut", "10:00:00")))
            task.setValue("eventTag", EVENT_TYPE_TO_TAG.get(rec.get("TaskType", "Task"), 3))

            try:
                task.setValue("timeFrame", int(rec.get("Classification", "2")))
            except Exception:
                task.setValue("timeFrame", 2)

            day_name = rec.get("Day", "Monday")
            task.setValue("day", day_name)

            tid = task_info.get("TaskID")
            for s in subtasks_map.get((tid, day_name), []):
                st_obj = subTask(
                    s.get("Subtask", "Subtask"),
                    s.get("SubtaskStatus") == "done"
                )
                task.addSubTask(st_obj)

            task.setPriority()
            week_instance.addTaskToDay(task, day_name)

        week_instance.organizeWeek()
    except Exception as e:
        print(f"Error loading tasks from Supabase: {e}")

    return week_instance

def add_task_to_json(task_dict):
    pass

def delete_task_from_json(task_id):
    pass

def update_task_in_json(task_id, updated_task_dict):
    pass

# ==================== RECURRENCE OPERATIONS ====================

def save_recurrences(recurrences):
    """Recurrence data is stored in Supabase — cache locally as fallback."""
    save_json("data/recurrences.json", recurrences)

def load_recurrences():
    """Derive recurrence map from Supabase Recurrence table."""
    try:
        result = supabase.table("Recurrence").select("Day, Tasks(TaskName)").execute()
        recurrences = {}
        for rec in result.data:
            task_info = rec.get("Tasks") or {}
            task_name = task_info.get("TaskName")
            day = rec.get("Day")
            if task_name and day:
                if task_name not in recurrences:
                    recurrences[task_name] = []
                if day not in recurrences[task_name]:
                    recurrences[task_name].append(day)
        return recurrences
    except Exception as e:
        print(f"Error loading recurrences from Supabase: {e}")
        return load_json("data/recurrences.json", default={})

# ==================== LINK/SHORTCUT OPERATIONS (JSON) ====================

def load_shortcuts():
    return load_json(LINKS_JSON, default=[
        {"id": str(uuid.uuid4()), "name": "Google Drive", "url": "https://drive.google.com"},
        {"id": str(uuid.uuid4()), "name": "Gmail", "url": "https://gmail.com"},
    ])

def save_shortcuts(shortcuts):
    return save_json(LINKS_JSON, shortcuts)

def add_shortcut(name, url):
    shortcuts = load_shortcuts()
    shortcuts.append({"id": str(uuid.uuid4()), "name": name, "url": url})
    return save_shortcuts(shortcuts)

def delete_shortcut(shortcut_id):
    shortcuts = load_shortcuts()
    shortcuts = [s for s in shortcuts if s.get("id") != shortcut_id]
    return save_shortcuts(shortcuts)

def update_shortcut(shortcut_id, name, url):
    shortcuts = load_shortcuts()
    for i, shortcut in enumerate(shortcuts):
        if shortcut.get("id") == shortcut_id:
            shortcuts[i] = {"id": shortcut_id, "name": name, "url": url}
            return save_shortcuts(shortcuts)
    return False

# ==================== NOTES OPERATIONS (JSON) ====================

def save_notes(task_notes):
    return save_json("data/notes.json", {
        "task_notes": task_notes,
        "last_updated": datetime.now().isoformat()
    })

def load_notes():
    data = load_json("data/notes.json", default={"task_notes": {}})
    return data.get("task_notes", {})

# ==================== SETTINGS OPERATIONS (JSON) ====================

def save_settings(settings):
    return save_json(SETTINGS_JSON, settings)

def load_settings():
    return load_json(SETTINGS_JSON, default={
        "theme": "dark",
        "default_view": "planner",
        "auto_save": True
    })

# ==================== HANDBOOK OPERATIONS (JSON) ====================

def save_handbook_notes(notes):
    return save_json("data/handbook_notes.json", {
        "notes": notes,
        "last_updated": datetime.now().isoformat()
    })

def load_handbook_notes():
    data = load_json("data/handbook_notes.json", default={"notes": ""})
    return data.get("notes", "")

# ==================== BACKUP OPERATIONS ====================

def create_backup():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = f"data/backups/{timestamp}"
    os.makedirs(backup_dir, exist_ok=True)

    files = [
        LINKS_JSON, SETTINGS_JSON,
        "data/notes.json", "data/recurrences.json",
        "data/handbook_notes.json", "data/subtasks.json"
    ]
    for filepath in files:
        if os.path.exists(filepath):
            data = load_json(filepath)
            save_json(f"{backup_dir}/{os.path.basename(filepath)}", data)
    return backup_dir

def list_backups():
    backup_dir = "data/backups"
    if os.path.exists(backup_dir):
        return sorted(os.listdir(backup_dir), reverse=True)
    return []

def restore_backup(backup_name):
    backup_dir = f"data/backups/{backup_name}"
    if not os.path.exists(backup_dir):
        return False
    for filename in os.listdir(backup_dir):
        data = load_json(f"{backup_dir}/{filename}")
        save_json(f"data/{filename}", data)
    return True

# ==================== UTILITY FUNCTIONS ====================

def clear_all_data():
    save_json(LINKS_JSON, [])
    save_json("data/notes.json", {"task_notes": {}})
    save_json("data/recurrences.json", {})
    save_json("data/handbook_notes.json", {"notes": ""})
    save_json("data/subtasks.json", {})
    return True

def get_statistics():
    w = load_tasks()
    tasks = [t for d in w.days for t in d.tasks]
    total_tasks = len(tasks)
    total_subtasks = sum(len(t.subTasks) for t in tasks)
    completed_subtasks = sum(sum(1 for s in t.subTasks if s.status) for t in tasks)
    tasks_by_day = {}
    for t in tasks:
        tasks_by_day[t.day] = tasks_by_day.get(t.day, 0) + 1
    return {
        "total_tasks": total_tasks,
        "total_subtasks": total_subtasks,
        "completed_subtasks": completed_subtasks,
        "completion_rate": round(
            (completed_subtasks / total_subtasks * 100) if total_subtasks > 0 else 0, 1
        ),
        "tasks_by_day": tasks_by_day,
    }

def export_to_text():
    w = load_tasks()
    output = [
        "=== BAREMINIMUM TASK EXPORT ===",
        f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        ""
    ]
    for day in w.days:
        if day.tasks:
            output.append(f"\n{'='*50}\n{day.name.upper()}\n{'='*50}")
            for task in day.tasks:
                output.append(f"\n• {task.taskName}")
                output.append(f"  Difficulty: {task.taskDifficulty}/5")
                s = task.timeStart
                e = task.timeEnd
                output.append(f"  Time: {s//60:02d}:{s%60:02d} - {e//60:02d}:{e%60:02d}")
                if task.subTasks:
                    output.append("  Subtasks:")
                    for sub in task.subTasks:
                        status = "✓" if sub.status else "○"
                        output.append(f"    {status} {sub.name}")
    return "\n".join(output)
