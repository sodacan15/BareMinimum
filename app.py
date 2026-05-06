import streamlit as st
from datetime import time, datetime
import sys
import time as t_lib

sys.path.append('.')

from dataStruct import Task, subTask, week
import functions as fn

st.set_page_config(page_title="BareMinimum", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    .stApp { background-color: #000; color: #fff; }
    #MainMenu, footer { visibility: hidden; }

    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&display=swap');
    html, body, [class*="css"] { font-family: 'IBM Plex Mono', monospace; color: #fff; font-size: 12px; }

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

    .main .block-container { padding: 1rem 1.5rem; max-width: 100%; }
    h1, h2, h3 { font-weight: 400; margin: 0; padding: 0; }
    h1 { font-size: 14px; } h2 { font-size: 13px; } h3 { font-size: 12px; }

    .stTabs [data-baseweb="tab-list"] { gap: 0; background-color: #000; border-bottom: 1px solid #fff; padding: 0; }
    .stTabs [data-baseweb="tab"] {
        background-color: #000; border: 1px solid #fff; border-bottom: none; color: #666;
        padding: 0.4rem 1rem; font-size: 10px; letter-spacing: 0.15em; margin: 0; height: 32px;
    }
    .stTabs [aria-selected="true"] { color: #fff; border-bottom: 1px solid #000; margin-bottom: -1px; }

    .stTextInput > div > div > input, .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select, .stTimeInput > div > div > input {
        background-color: #000; color: #fff; border: 1px solid #fff; border-radius: 0;
        font-size: 11px; padding: 0.3rem 0.5rem;
    }
    .stSlider { padding: 0; }

    .clock-text { font-size: 14px; color: #fff; margin-bottom: 10px; border-bottom: 1px solid #333; padding-bottom: 5px; }

    .stButton > button {
        background-color: #000; color: #fff; border: 1px solid #fff; border-radius: 0;
        padding: 0.3rem 0.6rem; font-size: 10px; letter-spacing: 0.1em;
    }
    .stButton > button:hover { background-color: #fff; color: #000; }

    .label-text { font-size: 9px; letter-spacing: 0.15em; color: #999; text-transform: uppercase; margin: 0.4rem 0 0.2rem 0; }
    .stProgress > div > div > div { background-color: #fff; height: 2px; }

    .custom-divider { border-top: 1px solid #222; margin: 0.6rem 0; }

    .task-status-badge {
        display: inline-block; padding: 2px 6px; font-size: 8px;
        border: 1px solid; margin-left: 5px; letter-spacing: 0.1em;
    }
    .status-done    { border-color: #0f0; color: #0f0; }
    .status-progress{ border-color: #ff0; color: #ff0; }
    .status-pending { border-color: #444; color: #444; }

    .task-detail {
        border: 1px solid #333;
        border-top: 2px solid #fff;
        padding: 1rem;
        margin-bottom: 0.5rem;
        background: #080808;
    }
    .meta-chip {
        display: inline-block; font-size: 8px; color: #666;
        border: 1px solid #333; padding: 1px 6px; margin-right: 4px;
        letter-spacing: 0.1em;
    }
</style>
""", unsafe_allow_html=True)

DIFFICULTY_MAP = {1: "Very Easy", 2: "Easy", 3: "Average", 4: "Hard", 5: "Very Hard"}
EVENT_TAGS      = {5: "Event", 4: "Assignment", 3: "Task", 1: "Chore"}
EVENT_TAGS_REV  = {v: k for k, v in EVENT_TAGS.items()}
TIME_FRAMES     = {1: "Morning", 2: "Afternoon", 3: "Evening", 4: "All Day"}

# ── Session state ────────────────────────────────────────────────────────────
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

if 'task_notes'        not in st.session_state: st.session_state.task_notes        = fn.load_notes()
if 'task_recurrences'  not in st.session_state: st.session_state.task_recurrences  = fn.load_recurrences()
if 'current_view'      not in st.session_state: st.session_state.current_view      = 'planner'
if 'selected_task_id'  not in st.session_state: st.session_state.selected_task_id  = None
if 'shortcuts'         not in st.session_state: st.session_state.shortcuts         = fn.load_shortcuts()
if 'handbook_notes'    not in st.session_state: st.session_state.handbook_notes    = fn.load_handbook_notes()
if 'auto_save'         not in st.session_state: st.session_state.auto_save         = True
if 'search_filter'     not in st.session_state: st.session_state.search_filter     = ""
if 'last_auto_save'    not in st.session_state: st.session_state.last_auto_save    = 0.0

# ── Helpers ──────────────────────────────────────────────────────────────────
def mins_to_time(minutes): return time(minutes // 60, minutes % 60)
def time_to_mins(t):       return t.hour * 60 + t.minute

def auto_time_frame(start, end):
    if end - start >= 480: return 4
    if start < 720:        return 1
    if start < 1020:       return 2
    return 3

def debounced_save():
    if st.session_state.auto_save:
        now = t_lib.time()
        if now - st.session_state.last_auto_save > 1.5:
            fn.save_tasks(st.session_state.week_instance)
            fn.save_notes(st.session_state.task_notes)
            fn.save_recurrences(st.session_state.task_recurrences)
            st.session_state.last_auto_save = now

def get_status_badge(task):
    p = task.getProgress()
    if p == 100: return '<span class="task-status-badge status-done">✓ DONE</span>'
    if p > 0:    return f'<span class="task-status-badge status-progress">{p:.0f}%</span>'
    return '<span class="task-status-badge status-pending">TODO</span>'

def get_instance(task_name, day_name):
    for d in st.session_state.week_instance.days:
        if d.name == day_name:
            for t in d.tasks:
                if t.taskName == task_name:
                    return t
    return None

def get_recurrence_days(task_name):
    if task_name not in st.session_state.task_recurrences:
        st.session_state.task_recurrences[task_name] = []
        for day in st.session_state.week_instance.days:
            for t in day.tasks:
                if t.taskName == task_name:
                    if day.name not in st.session_state.task_recurrences[task_name]:
                        st.session_state.task_recurrences[task_name].append(day.name)
    return st.session_state.task_recurrences[task_name]

def add_new_task(day_obj):
    t = Task()
    t.setValue("taskName", "New Task")
    t.setValue("day", day_obj.name)
    t.addSubTask(subTask("Subtask", False))
    t.setPriority()
    day_obj.addTask(t)
    st.session_state.week_instance.organizeWeek()
    if st.session_state.auto_save:
        fn.save_tasks(st.session_state.week_instance)

def add_recurrence(task_obj, day_name):
    name = task_obj.taskName
    if name not in st.session_state.task_recurrences:
        st.session_state.task_recurrences[name] = []
    if day_name not in st.session_state.task_recurrences[name]:
        st.session_state.task_recurrences[name].append(day_name)
        new_t = task_obj.clone()
        new_t.day = day_name
        st.session_state.week_instance.addTaskToDay(new_t, day_name)
        st.session_state.week_instance.organizeWeek()
        if st.session_state.auto_save:
            fn.save_tasks(st.session_state.week_instance)
            fn.save_recurrences(st.session_state.task_recurrences)

def remove_recurrence(task_name, day_name):
    if task_name in st.session_state.task_recurrences:
        if day_name in st.session_state.task_recurrences[task_name]:
            st.session_state.task_recurrences[task_name].remove(day_name)
            for day in st.session_state.week_instance.days:
                if day.name == day_name:
                    for t in day.tasks[:]:
                        if t.taskName == task_name:
                            day.removeTask(t); break
            st.session_state.week_instance.organizeWeek()
            if st.session_state.auto_save:
                fn.save_tasks(st.session_state.week_instance)
                fn.save_recurrences(st.session_state.task_recurrences)

def delete_task_by_id(task_id, task_name):
    for day in st.session_state.week_instance.days:
        for t in day.tasks[:]:
            if t.id == task_id:
                day.removeTask(t)
    elsewhere = any(t.taskName == task_name for d in st.session_state.week_instance.days for t in d.tasks)
    if not elsewhere:
        st.session_state.task_recurrences.pop(task_name, None)
        st.session_state.task_notes.pop(task_name, None)
    st.session_state.week_instance.organizeWeek()
    fn.save_tasks(st.session_state.week_instance)
    fn.save_recurrences(st.session_state.task_recurrences)
    fn.save_notes(st.session_state.task_notes)

# ── Inline task detail ────────────────────────────────────────────────────────
def render_task_detail(task):
    task_key = task.taskName
    if task_key not in st.session_state.task_notes:
        st.session_state.task_notes[task_key] = ""

    rec_days = get_recurrence_days(task_key)
    all_days  = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']

    st.markdown('<div class="task-detail">', unsafe_allow_html=True)

    # ── Header row ──
    hc1, hc2 = st.columns([5, 1])
    with hc1:
        st.markdown(f'<div class="label-text">Task Configuration</div>', unsafe_allow_html=True)
    with hc2:
        if st.button("✕ Close", key=f"close_{task.id}", use_container_width=True):
            st.session_state.selected_task_id = None
            st.rerun()

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # ── Recurrence tabs (one per day this task appears) ──
    if len(rec_days) > 1:
        rtabs = st.tabs([d[:3].upper() for d in rec_days])
    else:
        rtabs = [st.container()]

    for tab, d_name in zip(rtabs, rec_days):
        with tab:
            inst = get_instance(task_key, d_name)
            if not inst:
                st.warning(f"Instance for {d_name} missing.")
                continue
            _render_instance(inst, d_name, task_key, rec_days, all_days)

    st.markdown('</div>', unsafe_allow_html=True)
    debounced_save()


def _render_instance(inst, d_name, task_key, rec_days, all_days):
    uid = f"{inst.id}_{d_name}"

    # ── Name ──
    new_name = st.text_input("Name", inst.taskName, key=f"n_{uid}", label_visibility="collapsed")
    inst.setValue("taskName", new_name)

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # ── Time + auto time-frame ──
    st.markdown('<div class="label-text">Time Window</div>', unsafe_allow_html=True)
    tc1, tc2, tc3 = st.columns([2, 2, 3])
    with tc1:
        tin = st.time_input("Start", mins_to_time(inst.timeStart), key=f"ti_{uid}", label_visibility="collapsed")
        inst.setValue("timeStart", time_to_mins(tin))
    with tc2:
        tout = st.time_input("End", mins_to_time(inst.timeEnd), key=f"to_{uid}", label_visibility="collapsed")
        inst.setValue("timeEnd", time_to_mins(tout))
    with tc3:
        tf = auto_time_frame(inst.timeStart, inst.timeEnd)
        inst.setValue("timeFrame", tf)
        dur = inst.taskDuration
        st.markdown(
            f'<div style="padding-top:8px;font-size:9px;color:#666;">'
            f'{dur//60}h {dur%60:02d}m &nbsp;·&nbsp; {TIME_FRAMES.get(tf,"")}</div>',
            unsafe_allow_html=True
        )

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # ── Deadline + Type + Difficulty (compact row) ──
    dc1, dc2, dc3 = st.columns(3)
    with dc1:
        st.markdown('<div class="label-text">Deadline</div>', unsafe_allow_html=True)
        hard = st.radio("dl", ["Hard", "Soft"],
                        index=0 if inst.taskDeadline == 1 else 1,
                        key=f"dl_{uid}", horizontal=True, label_visibility="collapsed")
        inst.setValue("taskDeadline", 1 if hard == "Hard" else 0)
    with dc2:
        st.markdown('<div class="label-text">Type</div>', unsafe_allow_html=True)
        ev_list = ['Event', 'Assignment', 'Task', 'Chore']
        event = st.selectbox("Type", ev_list,
                             index=ev_list.index(EVENT_TAGS.get(inst.eventTag, "Task")),
                             key=f"et_{uid}", label_visibility="collapsed")
        inst.setValue("eventTag", EVENT_TAGS_REV[event])
    with dc3:
        st.markdown('<div class="label-text">Difficulty</div>', unsafe_allow_html=True)
        diff = st.slider("Diff", 1, 5, inst.taskDifficulty, key=f"df_{uid}", label_visibility="collapsed")
        inst.setValue("taskDifficulty", diff)

    inst.setPriority()
    st.markdown(
        f'<div style="margin-top:4px;">'
        f'<span class="meta-chip">Priority {inst.priority}%</span>'
        f'<span class="meta-chip">{DIFFICULTY_MAP.get(diff,"")}</span>'
        f'</div>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # ── Subtasks ──
    st.markdown('<div class="label-text">Subtasks</div>', unsafe_allow_html=True)
    progress = inst.getProgress()
    st.progress(progress / 100)

    to_remove = []
    for i, sub in enumerate(inst.subTasks):
        sk = f"{inst.id}_{sub.id}_{d_name}_{i}"
        c1, c2, c3 = st.columns([1, 8, 1])
        with c1:
            done = st.checkbox("", value=sub.status, key=f"sd_{sk}", label_visibility="collapsed")
            if done != sub.status:
                sub.markDone() if done else sub.markUndone()
        with c2:
            new_sn = st.text_input("", value=sub.name, key=f"st_{sk}", label_visibility="collapsed")
            if new_sn != sub.name:
                sub.name = new_sn
        with c3:
            if st.button("×", key=f"ds_{sk}"):
                to_remove.append(sub)

    if to_remove:
        for sub in to_remove:
            inst.removeSubTask(sub)
        fn.save_tasks(st.session_state.week_instance)
        st.rerun()

    if st.button("+ Subtask", key=f"as_{uid}"):
        inst.addSubTask(subTask("New subtask", False))
        fn.save_tasks(st.session_state.week_instance)
        st.rerun()

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # ── Notes ──
    st.markdown('<div class="label-text">Notes</div>', unsafe_allow_html=True)
    st.session_state.task_notes[task_key] = st.text_area(
        "notes", st.session_state.task_notes[task_key],
        height=80, key=f"nt_{uid}", label_visibility="collapsed"
    )

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # ── Schedule (recurrence management) ──
    st.markdown('<div class="label-text">Schedule</div>', unsafe_allow_html=True)
    avail = [d for d in all_days if d not in rec_days]
    if avail:
        sc1, sc2 = st.columns([4, 1])
        with sc1:
            new_day = st.selectbox("Add to", ["--"] + avail, key=f"add_day_{uid}", label_visibility="collapsed")
        with sc2:
            if st.button("+", key=f"add_day_btn_{uid}") and new_day != "--":
                add_recurrence(inst, new_day)
                st.rerun()

    if len(rec_days) > 1:
        if st.button(f"Remove {d_name} instance", key=f"rm_{uid}"):
            remove_recurrence(task_key, d_name)
            st.session_state.selected_task_id = None
            st.rerun()

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # ── Actions ──
    ac1, ac2, ac3 = st.columns(3)
    with ac1:
        if st.button("💾 Save", key=f"save_{uid}", use_container_width=True):
            st.session_state.week_instance.organizeWeek()
            fn.save_tasks(st.session_state.week_instance)
            fn.save_notes(st.session_state.task_notes)
            fn.save_recurrences(st.session_state.task_recurrences)
            fn.save_handbook_notes(st.session_state.handbook_notes)
            fn.save_shortcuts(st.session_state.shortcuts)
            st.success("✓ Saved")
    with ac2:
        pass
    with ac3:
        if st.button("🗑️ Delete", key=f"del_{uid}", use_container_width=True):
            delete_task_by_id(inst.id, task_key)
            st.session_state.selected_task_id = None
            st.rerun()


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("# BareMinimum")
    st.markdown(f'<div class="clock-text">{datetime.now().strftime("%H:%M:%S")}</div>', unsafe_allow_html=True)
    st.session_state.search_filter = st.text_input(
        "Filter", value=st.session_state.search_filter,
        placeholder="Search tasks...", label_visibility="collapsed"
    )
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    if st.button("📅 Planner"):   st.session_state.current_view = 'planner';   st.rerun()
    if st.button("🕒 Timetable"): st.session_state.current_view = 'timetable'; st.rerun()
    if st.button("📖 Handbook"):  st.session_state.current_view = 'handbook';  st.rerun()
    if st.button("📊 Progress"):  st.session_state.current_view = 'progress';  st.rerun()
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    if st.button("💾 SAVE STATE", use_container_width=True):
        fn.save_tasks(st.session_state.week_instance)
        fn.save_notes(st.session_state.task_notes)
        fn.save_recurrences(st.session_state.task_recurrences)
        fn.save_shortcuts(st.session_state.shortcuts)
        fn.save_handbook_notes(st.session_state.handbook_notes)
        st.success("Saved")
    if st.button("📄 EXPORT", use_container_width=True):
        st.download_button("Download", fn.export_to_text(),
                           f"export_{datetime.now().strftime('%Y%m%d')}.txt", "text/plain")
    if st.button("🔄 BACKUP", use_container_width=True):
        fn.create_backup(); st.success("Backup done")
    st.session_state.auto_save = st.checkbox(
        "Auto-save", value=st.session_state.auto_save, key="auto_save_toggle"
    )

# ── Views ─────────────────────────────────────────────────────────────────────
if st.session_state.current_view == 'planner':
    days_short = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
    days_full  = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    today_name = datetime.now().strftime("%A")

    left_col, right_col = st.columns([1, 1])

    with left_col:
        sort_choice = st.selectbox(
            "Sort", ["Priority", "Difficulty", "Time", "Status"],
            label_visibility="collapsed"
        )
        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

        day_labels = []
        for i, (ds, df) in enumerate(zip(days_short, days_full)):
            cnt    = len(st.session_state.week_instance.days[i].tasks)
            dot    = "● " if df == today_name else ""
            suffix = f"·{cnt}" if cnt else ""
            day_labels.append(f"{dot}{ds}{suffix}")

        day_tabs = st.tabs(day_labels)

        for i, (d_short, d_full) in enumerate(zip(days_short, days_full)):
            day_obj = st.session_state.week_instance.days[i]
            with day_tabs[i]:
                tasks = list(day_obj.tasks)
                sf = st.session_state.search_filter.lower()
                if sf:
                    tasks = [t for t in tasks if sf in t.taskName.lower()]

                if sort_choice == "Priority":     tasks.sort(key=lambda x: x.priority, reverse=True)
                elif sort_choice == "Difficulty": tasks.sort(key=lambda x: x.taskDifficulty, reverse=True)
                elif sort_choice == "Time":       tasks.sort(key=lambda x: x.timeStart)
                elif sort_choice == "Status":     tasks.sort(key=lambda x: x.getProgress())

                if not tasks:
                    st.markdown('<div style="color:#444;font-size:10px;padding:8px 0;">— empty —</div>', unsafe_allow_html=True)
                else:
                    last_cat = None
                    for t in tasks:
                        cat = None
                        if sort_choice == "Priority":
                            cat = "HIGH" if t.priority >= 80 else ("MID" if t.priority >= 55 else "LOW")
                        elif sort_choice == "Status":
                            p = t.getProgress()
                            cat = "DONE" if p == 100 else ("IN PROGRESS" if p > 0 else "TODO")

                        if cat and cat != last_cat:
                            st.markdown(f'<div class="label-text" style="color:#555;margin-top:8px;">{cat}</div>', unsafe_allow_html=True)
                            last_cat = cat

                        t_str    = mins_to_time(t.timeStart).strftime("%H:%M")
                        prog     = t.getProgress()
                        tag      = EVENT_TAGS.get(t.eventTag, "Task")
                        is_sel   = st.session_state.selected_task_id == t.id

                        rc1, rc2 = st.columns([6, 1])
                        with rc1:
                            label = f"{'▶' if not is_sel else '▷'} [{t_str}] {t.taskName}"
                            if st.button(label, key=f"sel_{t.id}", use_container_width=True):
                                st.session_state.selected_task_id = None if is_sel else t.id
                                st.rerun()
                        with rc2:
                            if prog == 100:
                                st.markdown('<span class="task-status-badge status-done" style="font-size:7px;">✓</span>', unsafe_allow_html=True)
                            elif prog > 0:
                                st.markdown(f'<span class="task-status-badge status-progress" style="font-size:7px;">{prog:.0f}%</span>', unsafe_allow_html=True)
                            else:
                                st.markdown(f'<span class="task-status-badge status-pending" style="font-size:7px;">{tag[:3].upper()}</span>', unsafe_allow_html=True)

                st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
                if st.button(f"+ ADD TO {d_short}", key=f"add_{d_full}", use_container_width=True):
                    add_new_task(day_obj)
                    st.rerun()

    with right_col:
        if st.session_state.selected_task_id:
            selected_task = None
            for day in st.session_state.week_instance.days:
                for t in day.tasks:
                    if t.id == st.session_state.selected_task_id:
                        selected_task = t
                        break
                if selected_task:
                    break
            if selected_task:
                render_task_detail(selected_task)
            else:
                st.session_state.selected_task_id = None
        else:
            st.markdown(
                '<div style="color:#333;font-size:10px;padding-top:4rem;text-align:center;">'
                'select a task to edit</div>',
                unsafe_allow_html=True
            )


elif st.session_state.current_view == 'timetable':
    st.markdown("### WEEKLY TIMETABLE")
    st.markdown('<div class="label-text">Chronological schedule — all tasks this week</div>', unsafe_allow_html=True)
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    TYPE_COLORS = {"Event": "#4af", "Assignment": "#f94", "Task": "#fff", "Chore": "#888"}
    days_full   = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    today_name  = datetime.now().strftime("%A")

    active_days = [
        d_name for d_name in days_full
        for d in st.session_state.week_instance.days
        if d.name == d_name and d.tasks
    ]

    if not active_days:
        st.info("No tasks scheduled this week.")
    else:
        tt_tabs = st.tabs([
            ("● " if d == today_name else "") + d[:3].upper()
            for d in active_days
        ])
        for tab, day_name in zip(tt_tabs, active_days):
            with tab:
                day_obj      = next(d for d in st.session_state.week_instance.days if d.name == day_name)
                sorted_tasks = sorted(day_obj.tasks, key=lambda x: x.timeStart)
                total_mins   = sum(tk.taskDuration for tk in sorted_tasks)
                th, tm       = total_mins // 60, total_mins % 60
                is_today     = day_name == today_name

                today_badge = '&nbsp;&nbsp;<span style="color:#0f0;">● TODAY</span>' if is_today else ""
                st.markdown(
                    f'<div style="font-size:9px;color:#666;margin-bottom:8px;">'
                    f'{len(sorted_tasks)} tasks &nbsp;·&nbsp; {th}h {tm:02d}m total{today_badge}'
                    f'</div>',
                    unsafe_allow_html=True
                )

                for task in sorted_tasks:
                    start_str = mins_to_time(task.timeStart).strftime("%H:%M")
                    end_str   = mins_to_time(task.timeEnd).strftime("%H:%M")
                    dur_h = task.taskDuration // 60
                    dur_m = task.taskDuration % 60
                    dur_str   = f"{dur_h}h {dur_m}m" if dur_h else f"{dur_m}m"
                    progress  = task.getProgress()
                    bar_w     = max(int(progress), 3)
                    bar_color = "#0f0" if progress == 100 else ("#ff0" if progress > 0 else "#333")
                    tag       = EVENT_TAGS.get(task.eventTag, "Task")
                    name_color= TYPE_COLORS.get(tag, "#fff")
                    n_subs    = len(task.subTasks)
                    done_subs = sum(1 for s in task.subTasks if s.status)
                    sub_str   = f"{done_subs}/{n_subs} subtasks" if n_subs else "no subtasks"

                    c1, c2, c3 = st.columns([2, 5, 2])
                    with c1:
                        st.markdown(
                            f'<div style="font-size:9px;color:#666;padding-top:4px;">'
                            f'{start_str}<br/>{end_str}</div>',
                            unsafe_allow_html=True
                        )
                    with c2:
                        st.markdown(
                            f'<div style="font-size:11px;color:{name_color};margin-bottom:4px;">{task.taskName}</div>'
                            f'<div style="height:2px;background:#222;border-radius:1px;">'
                            f'<div style="height:2px;background:{bar_color};width:{bar_w}%;"></div></div>'
                            f'<div style="font-size:8px;color:#555;margin-top:2px;">{tag} · {sub_str}</div>',
                            unsafe_allow_html=True
                        )
                    with c3:
                        pct_col = "#0f0" if progress == 100 else ("#ff0" if progress > 0 else "#555")
                        st.markdown(
                            f'<div style="font-size:9px;color:#666;text-align:right;padding-top:4px;">'
                            f'{dur_str}<br/>'
                            f'<span style="color:{pct_col};">{progress:.0f}%</span></div>',
                            unsafe_allow_html=True
                        )
                    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)


elif st.session_state.current_view == 'handbook':
    handbook_tabs = st.tabs(["SHORTCUTS", "NOTEPAD"])
    with handbook_tabs[0]:
        st.markdown('<div class="label-text">External Links</div>', unsafe_allow_html=True)

        for idx, shortcut in enumerate(st.session_state.shortcuts):
            c1, c2 = st.columns([5, 1])
            with c1:
                url = shortcut["url"]
                if not url.startswith("http"):
                    url = "https://" + url
                st.link_button(shortcut["name"], url, use_container_width=True)
            with c2:
                if st.button("✕", key=f"del_s_{shortcut.get('id', idx)}", use_container_width=True):
                    fn.delete_shortcut(shortcut.get('id', idx))
                    st.session_state.shortcuts = fn.load_shortcuts()
                    st.rerun()
            st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

        with st.expander("+ Add Link"):
            n_name = st.text_input("Name", key="new_s_name")
            n_url  = st.text_input("URL",  key="new_s_url")
            if st.button("Save Link", use_container_width=True):
                if n_name and n_url:
                    fn.add_shortcut(n_name, n_url)
                    st.session_state.shortcuts = fn.load_shortcuts()
                    st.rerun()

    with handbook_tabs[1]:
        st.markdown('<div class="label-text">Central Notepad</div>', unsafe_allow_html=True)
        notes = st.text_area("", height=420, value=st.session_state.handbook_notes,
                             key="notepad", label_visibility="collapsed")
        if notes != st.session_state.handbook_notes:
            st.session_state.handbook_notes = notes
            fn.save_handbook_notes(notes)


elif st.session_state.current_view == 'progress':
    tasks      = [t for d in st.session_state.week_instance.days for t in d.tasks]
    total_subs = sum(len(t.subTasks) for t in tasks)
    done_subs  = sum(sum(1 for s in t.subTasks if s.status) for t in tasks)

    st.markdown("### PRODUCTIVITY OVERVIEW")
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    prog_pct = (done_subs / total_subs * 100) if total_subs > 0 else 0
    st.progress(prog_pct / 100)
    st.markdown(
        f'<div style="font-size:10px;color:#666;margin:4px 0 12px;">'
        f'{done_subs}/{total_subs} subtasks &nbsp;·&nbsp; {prog_pct:.1f}% complete</div>',
        unsafe_allow_html=True
    )
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="label-text">In Progress</div>', unsafe_allow_html=True)
        in_prog = [t for t in tasks if 0 < sum(1 for s in t.subTasks if s.status) < len(t.subTasks)]
        if not in_prog:
            st.markdown('<div style="color:#444;font-size:10px;">None</div>', unsafe_allow_html=True)
        for t in in_prog:
            p = t.getProgress()
            st.markdown(
                f'<div style="font-size:10px;margin-bottom:4px;">{t.taskName}'
                f'<span style="color:#ff0;font-size:8px;margin-left:6px;">{p:.0f}%</span></div>',
                unsafe_allow_html=True
            )
    with c2:
        st.markdown('<div class="label-text">Completed</div>', unsafe_allow_html=True)
        completed = [t for t in tasks if t.subTasks and all(s.status for s in t.subTasks)]
        if not completed:
            st.markdown('<div style="color:#444;font-size:10px;">None</div>', unsafe_allow_html=True)
        for t in completed:
            st.markdown(
                f'<div style="font-size:10px;color:#0f0;margin-bottom:4px;">✓ {t.taskName}</div>',
                unsafe_allow_html=True
            )

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="label-text">By Day</div>', unsafe_allow_html=True)
    days_full = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    for day_obj in st.session_state.week_instance.days:
        day_tasks = day_obj.tasks
        if not day_tasks:
            continue
        day_subs  = sum(len(t.subTasks) for t in day_tasks)
        day_done  = sum(sum(1 for s in t.subTasks if s.status) for t in day_tasks)
        day_pct   = (day_done / day_subs * 100) if day_subs > 0 else 0
        st.markdown(
            f'<div style="display:flex;justify-content:space-between;font-size:9px;color:#666;margin-bottom:2px;">'
            f'<span>{day_obj.name[:3].upper()}</span>'
            f'<span>{len(day_tasks)} tasks · {day_done}/{day_subs} sub · {day_pct:.0f}%</span></div>',
            unsafe_allow_html=True
        )
        st.progress(day_pct / 100)
