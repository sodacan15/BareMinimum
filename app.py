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
        background-color: #000; border-right: 1px solid #fff;
        min-width: 165px !important; max-width: 165px !important;
    }
    [data-testid="stSidebar"] > div:first-child { background-color: #000; padding: 1rem 0.5rem; }
    [data-testid="stSidebar"] h1 { font-size: 16px; font-weight: 400; padding: 0.8rem; margin: 0; border-bottom: 1px solid #fff; }
    [data-testid="stSidebar"] .stButton > button {
        background-color: #000; color: #fff; border: 1px solid #fff; border-radius: 0;
        padding: 0.5rem; font-size: 11px; width: 100%; text-align: left; margin-bottom: 0;
    }
    [data-testid="stSidebar"] .stButton > button:hover { background-color: #fff; color: #000; }

    .main .block-container { padding: 1rem 1.5rem; max-width: 100%; }
    h1,h2,h3 { font-weight: 400; margin: 0; padding: 0; }
    h1 { font-size: 14px; } h2 { font-size: 13px; } h3 { font-size: 12px; }

    .stTabs [data-baseweb="tab-list"] { gap: 0; background-color: #000; border-bottom: 1px solid #fff; padding: 0; }
    .stTabs [data-baseweb="tab"] {
        background-color: #000; border: 1px solid #fff; border-bottom: none; color: #555;
        padding: 0.4rem 0.8rem; font-size: 10px; letter-spacing: 0.12em; margin: 0; height: 32px;
    }
    .stTabs [aria-selected="true"] { color: #fff; border-bottom: 1px solid #000; margin-bottom: -1px; background: #111; }

    .stTextInput > div > div > input, .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select, .stTimeInput > div > div > input {
        background-color: #000; color: #fff; border: 1px solid #333; border-radius: 0;
        font-size: 11px; padding: 0.3rem 0.5rem;
    }
    .stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus {
        border-color: #fff !important;
    }
    .stSlider { padding: 0; }

    .clock-text { font-size: 13px; color: #888; margin-bottom: 8px; border-bottom: 1px solid #222; padding-bottom: 5px; }

    .stButton > button {
        background-color: #000; color: #fff; border: 1px solid #333; border-radius: 0;
        padding: 0.3rem 0.6rem; font-size: 10px; letter-spacing: 0.08em;
    }
    .stButton > button:hover { background-color: #fff; color: #000; border-color: #fff; }

    .label-text { font-size: 9px; letter-spacing: 0.15em; color: #555; text-transform: uppercase; margin: 0.4rem 0 0.2rem 0; }
    .stProgress > div > div > div { background-color: #fff; height: 2px; }
    .custom-divider { border-top: 1px solid #1a1a1a; margin: 0.6rem 0; }

    .task-row {
        border-left: 2px solid transparent;
        padding-left: 4px;
        margin-bottom: 2px;
    }
    .task-row-event      { border-left-color: #4af; }
    .task-row-assignment { border-left-color: #f94; }
    .task-row-chore      { border-left-color: #666; }
    .task-row-task       { border-left-color: #fff; }

    .task-status-badge {
        display: inline-block; padding: 1px 5px; font-size: 8px;
        border: 1px solid; letter-spacing: 0.08em;
    }
    .status-done     { border-color: #0f0; color: #0f0; }
    .status-progress { border-color: #ff0; color: #ff0; }
    .status-pending  { border-color: #333; color: #444; }

    .task-detail {
        border: 1px solid #222; border-top: 2px solid #fff;
        padding: 1rem; background: #060606;
    }
    .meta-chip {
        display: inline-block; font-size: 8px; color: #555;
        border: 1px solid #222; padding: 1px 5px; margin-right: 3px; letter-spacing: 0.08em;
    }
    .urgent-badge {
        display: inline-block; font-size: 8px; color: #f94;
        border: 1px solid #f94; padding: 1px 5px; margin-left: 4px;
    }
    .countdown-now { color: #0f0; font-size: 8px; }
    .countdown-soon { color: #ff0; font-size: 8px; }
    .countdown-later { color: #555; font-size: 8px; }

    .heatmap-cell {
        text-align: center; padding: 6px 2px; font-size: 9px;
        letter-spacing: 0.05em;
    }
    .search-result-row {
        border-left: 2px solid #555; padding: 4px 8px;
        margin-bottom: 4px; background: #080808; font-size: 10px;
    }
    .priority-bar-track {
        background: #1a1a1a; height: 3px; margin: 2px 0;
    }
    .template-chip {
        display: inline-block; font-size: 8px; color: #4af;
        border: 1px solid #4af; padding: 1px 6px; margin: 2px; cursor: pointer;
    }
</style>
""", unsafe_allow_html=True)

# ── Constants ─────────────────────────────────────────────────────────────────
DIFFICULTY_MAP  = {1: "Very Easy", 2: "Easy", 3: "Average", 4: "Hard", 5: "Very Hard"}
EVENT_TAGS      = {5: "Event", 4: "Assignment", 3: "Task", 1: "Chore"}
EVENT_TAGS_REV  = {v: k for k, v in EVENT_TAGS.items()}
TIME_FRAMES     = {1: "Morning", 2: "Afternoon", 3: "Evening", 4: "All Day"}
TYPE_COLORS     = {"Event": "#4af", "Assignment": "#f94", "Task": "#fff", "Chore": "#777"}
TYPE_ROW_CLASS  = {"Event": "task-row-event", "Assignment": "task-row-assignment",
                   "Task": "task-row-task",   "Chore": "task-row-chore"}
DAYS_FULL       = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']

# ── Session state ─────────────────────────────────────────────────────────────
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

if 'task_notes'       not in st.session_state: st.session_state.task_notes       = fn.load_notes()
if 'task_recurrences' not in st.session_state: st.session_state.task_recurrences = fn.load_recurrences()
if 'current_view'     not in st.session_state: st.session_state.current_view     = 'planner'
if 'selected_task_id' not in st.session_state: st.session_state.selected_task_id = None
if 'shortcuts'        not in st.session_state: st.session_state.shortcuts        = fn.load_shortcuts()
if 'handbook_notes'   not in st.session_state: st.session_state.handbook_notes   = fn.load_handbook_notes()
if 'auto_save'        not in st.session_state: st.session_state.auto_save        = True
if 'search_filter'    not in st.session_state: st.session_state.search_filter    = ""
if 'last_auto_save'   not in st.session_state: st.session_state.last_auto_save   = 0.0
if 'task_templates'   not in st.session_state: st.session_state.task_templates   = fn.load_templates()

# ── Helpers ───────────────────────────────────────────────────────────────────
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

def countdown_label(task, day_name):
    today = datetime.now().strftime("%A")
    if day_name != today:
        return ""
    now_mins = datetime.now().hour * 60 + datetime.now().minute
    s, e = task.timeStart, task.timeEnd
    if s <= now_mins <= e:
        return '<span class="countdown-now">● NOW</span>'
    elif now_mins < s:
        diff = s - now_mins
        h, m = diff // 60, diff % 60
        label = f"in {h}h{m:02d}m" if h else f"in {m}m"
        cls = "countdown-soon" if diff < 60 else "countdown-later"
        return f'<span class="{cls}">{label}</span>'
    else:
        return '<span class="countdown-later">past</span>'

def priority_breakdown(task):
    tf_scores  = {1: 12, 2: 8, 3: 4, 4: 15}
    dl_scores  = {1: 20, 0: 10}
    diff_scores = {1: 5, 2: 10, 3: 15, 4: 20, 5: 25}
    et_scores  = {5: 30, 4: 22, 3: 15, 1: 8}
    sc = len(task.subTasks)
    sub_score  = 3 if sc <= 2 else (6 if sc <= 5 else (8 if sc <= 8 else 10))
    return {
        "Time Frame":  tf_scores.get(task.timeFrame, 8),
        "Deadline":    dl_scores.get(task.taskDeadline, 10),
        "Difficulty":  diff_scores.get(task.taskDifficulty, 15),
        "Event Type":  et_scores.get(task.eventTag, 15),
        "Subtasks":    sub_score,
    }

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

def add_new_task(day_obj, template=None):
    t = Task()
    t.setValue("taskName", "New Task")
    t.setValue("day", day_obj.name)
    if template:
        t.setValue("taskDifficulty", template.get("difficulty", 3))
        t.setValue("timeStart",      template.get("timeStart", 540))
        t.setValue("timeEnd",        template.get("timeEnd", 600))
        t.setValue("eventTag",       template.get("eventTag", 3))
        for sn in template.get("subTasks", []):
            t.addSubTask(subTask(sn, False))
    else:
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
        # clean up all per-day notes for this task
        keys_to_del = [k for k in st.session_state.task_notes if k.startswith(f"{task_name}_")]
        for k in keys_to_del:
            del st.session_state.task_notes[k]
    st.session_state.week_instance.organizeWeek()
    fn.save_tasks(st.session_state.week_instance)
    fn.save_recurrences(st.session_state.task_recurrences)
    fn.save_notes(st.session_state.task_notes)

# ── Task detail panel ─────────────────────────────────────────────────────────
def render_task_detail(task):
    task_key = task.taskName
    rec_days = get_recurrence_days(task_key)

    st.markdown('<div class="task-detail">', unsafe_allow_html=True)

    hc1, hc2 = st.columns([5, 1])
    with hc1:
        tag = EVENT_TAGS.get(task.eventTag, "Task")
        col = TYPE_COLORS.get(tag, "#fff")
        st.markdown(
            f'<span style="color:{col};font-size:9px;letter-spacing:0.15em;">{tag.upper()}</span>'
            f'<span style="color:#333;font-size:9px;"> ── TASK CONFIG</span>',
            unsafe_allow_html=True
        )
    with hc2:
        if st.button("✕", key=f"close_{task.id}", use_container_width=True):
            st.session_state.selected_task_id = None
            st.rerun()

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

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
            _render_instance(inst, d_name, task_key, rec_days)

    st.markdown('</div>', unsafe_allow_html=True)
    debounced_save()


def _render_instance(inst, d_name, task_key, rec_days):
    uid      = f"{inst.id}_{d_name}"
    note_key = f"{task_key}_{d_name}"
    if note_key not in st.session_state.task_notes:
        st.session_state.task_notes[note_key] = ""

    # ── Name ──
    new_name = st.text_input("Name", inst.taskName, key=f"n_{uid}", label_visibility="collapsed")
    inst.setValue("taskName", new_name)

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # ── Time ──
    st.markdown('<div class="label-text">Time Window</div>', unsafe_allow_html=True)
    tc1, tc2, tc3 = st.columns([2, 2, 3])
    with tc1:
        tin = st.time_input("Start", mins_to_time(inst.timeStart), key=f"ti_{uid}", label_visibility="collapsed")
        inst.setValue("timeStart", time_to_mins(tin))
    with tc2:
        tout = st.time_input("End", mins_to_time(inst.timeEnd), key=f"to_{uid}", label_visibility="collapsed")
        inst.setValue("timeEnd", time_to_mins(tout))
    with tc3:
        tf  = auto_time_frame(inst.timeStart, inst.timeEnd)
        inst.setValue("timeFrame", tf)
        dur = inst.taskDuration
        st.markdown(
            f'<div style="padding-top:8px;font-size:9px;color:#555;">'
            f'{dur//60}h {dur%60:02d}m · {TIME_FRAMES.get(tf,"")}</div>',
            unsafe_allow_html=True
        )

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # ── Deadline + Type + Difficulty ──
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
        event   = st.selectbox("Type", ev_list,
                               index=ev_list.index(EVENT_TAGS.get(inst.eventTag, "Task")),
                               key=f"et_{uid}", label_visibility="collapsed")
        inst.setValue("eventTag", EVENT_TAGS_REV[event])
    with dc3:
        st.markdown('<div class="label-text">Difficulty</div>', unsafe_allow_html=True)
        diff = st.slider("Diff", 1, 5, inst.taskDifficulty, key=f"df_{uid}", label_visibility="collapsed")
        inst.setValue("taskDifficulty", diff)

    inst.setPriority()

    # ── Priority chips + breakdown ──
    st.markdown(
        f'<div style="margin:4px 0;">'
        f'<span class="meta-chip">Priority {inst.priority}%</span>'
        f'<span class="meta-chip">{DIFFICULTY_MAP.get(diff,"")}</span>'
        f'<span class="meta-chip">{TIME_FRAMES.get(tf,"")}</span>'
        f'</div>',
        unsafe_allow_html=True
    )
    with st.expander("Priority breakdown", expanded=False):
        breakdown = priority_breakdown(inst)
        total     = sum(breakdown.values())
        for factor, score in breakdown.items():
            pct = int(score / 100 * 100) if total else 0
            bar_w = int(score / max(breakdown.values()) * 100)
            st.markdown(
                f'<div style="display:flex;justify-content:space-between;font-size:8px;color:#666;margin-bottom:1px;">'
                f'<span>{factor}</span><span>{score} pts</span></div>'
                f'<div class="priority-bar-track">'
                f'<div style="height:3px;background:#fff;width:{bar_w}%;"></div></div>',
                unsafe_allow_html=True
            )

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # ── Subtasks ──
    st.markdown('<div class="label-text">Subtasks</div>', unsafe_allow_html=True)
    progress = inst.getProgress()
    st.progress(progress / 100)
    st.markdown(
        f'<div style="font-size:8px;color:#555;margin-bottom:4px;">{progress:.0f}% complete</div>',
        unsafe_allow_html=True
    )

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

    ba1, ba2 = st.columns(2)
    with ba1:
        if st.button("+ Subtask", key=f"as_{uid}", use_container_width=True):
            inst.addSubTask(subTask("New subtask", False))
            fn.save_tasks(st.session_state.week_instance)
            st.rerun()
    with ba2:
        if inst.subTasks and progress < 100:
            if st.button("✓ Mark All Done", key=f"mad_{uid}", use_container_width=True):
                for sub in inst.subTasks:
                    sub.markDone()
                fn.save_tasks(st.session_state.week_instance)
                st.rerun()

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # ── Notes (per task-day) ──
    st.markdown('<div class="label-text">Notes</div>', unsafe_allow_html=True)
    st.session_state.task_notes[note_key] = st.text_area(
        "notes", st.session_state.task_notes[note_key],
        height=80, key=f"nt_{uid}", label_visibility="collapsed"
    )

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # ── Schedule ──
    st.markdown('<div class="label-text">Schedule</div>', unsafe_allow_html=True)
    avail = [d for d in DAYS_FULL if d not in rec_days]
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

    # ── Template save ──
    with st.expander("Save as Template"):
        tpl_name = st.text_input("Template name", key=f"tpl_name_{uid}", placeholder="e.g. Class day")
        if st.button("Save Template", key=f"tpl_save_{uid}", use_container_width=True):
            if tpl_name:
                st.session_state.task_templates[tpl_name] = {
                    "difficulty": inst.taskDifficulty,
                    "timeStart":  inst.timeStart,
                    "timeEnd":    inst.timeEnd,
                    "eventTag":   inst.eventTag,
                    "subTasks":   [s.name for s in inst.subTasks],
                }
                fn.save_templates(st.session_state.task_templates)
                st.success(f"Template '{tpl_name}' saved")

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # ── Actions ──
    ac1, ac2 = st.columns(2)
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
        if st.button("🗑️ Delete", key=f"del_{uid}", use_container_width=True):
            delete_task_by_id(inst.id, task_key)
            st.session_state.selected_task_id = None
            st.rerun()


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("# BareMinimum")
    st.markdown(
        f'<div class="clock-text">{datetime.now().strftime("%a %H:%M")}</div>',
        unsafe_allow_html=True
    )
    st.session_state.search_filter = st.text_input(
        "Filter", value=st.session_state.search_filter,
        placeholder="Search all tasks...", label_visibility="collapsed"
    )
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    if st.button("📅 Planner"):   st.session_state.current_view = 'planner';   st.rerun()
    if st.button("🕒 Timetable"): st.session_state.current_view = 'timetable'; st.rerun()
    if st.button("📖 Handbook"):  st.session_state.current_view = 'handbook';  st.rerun()
    if st.button("📊 Progress"):  st.session_state.current_view = 'progress';  st.rerun()
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # Templates
    if st.session_state.task_templates:
        st.markdown('<div class="label-text">Templates</div>', unsafe_allow_html=True)
        for tname in list(st.session_state.task_templates.keys()):
            tc1, tc2 = st.columns([4, 1])
            with tc1:
                st.markdown(f'<div class="template-chip">{tname}</div>', unsafe_allow_html=True)
            with tc2:
                if st.button("✕", key=f"del_tpl_{tname}"):
                    del st.session_state.task_templates[tname]
                    fn.save_templates(st.session_state.task_templates)
                    st.rerun()
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
    days_short = ['MON','TUE','WED','THU','FRI','SAT','SUN']
    today_name = datetime.now().strftime("%A")
    sf         = st.session_state.search_filter.strip().lower()

    left_col, right_col = st.columns([1, 1])

    with left_col:
        # ── Global search results ──
        if sf:
            st.markdown(f'<div class="label-text">Search: "{sf}"</div>', unsafe_allow_html=True)
            any_found = False
            for day in st.session_state.week_instance.days:
                for t in day.tasks:
                    if sf in t.taskName.lower():
                        any_found   = True
                        tag         = EVENT_TAGS.get(t.eventTag, "Task")
                        col         = TYPE_COLORS.get(tag, "#fff")
                        prog        = t.getProgress()
                        t_str       = mins_to_time(t.timeStart).strftime("%H:%M")
                        prog_color  = "#0f0" if prog == 100 else ("#ff0" if prog > 0 else "#333")
                        is_sel      = st.session_state.selected_task_id == t.id
                        sr1, sr2 = st.columns([7, 1])
                        with sr1:
                            st.markdown(
                                f'<div class="search-result-row" style="border-left-color:{col};">'
                                f'<span style="color:{col};">{day.name[:3].upper()}</span>'
                                f' [{t_str}] {t.taskName}'
                                f'<div style="height:2px;background:#111;margin-top:3px;">'
                                f'<div style="height:2px;background:{prog_color};width:{max(int(prog),2)}%;"></div></div>'
                                f'</div>',
                                unsafe_allow_html=True
                            )
                        with sr2:
                            if st.button("▶", key=f"sr_sel_{t.id}", use_container_width=True):
                                st.session_state.selected_task_id = None if is_sel else t.id
                                st.rerun()
            if not any_found:
                st.markdown('<div style="color:#333;font-size:10px;">No results</div>', unsafe_allow_html=True)
            st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

        sort_choice = st.selectbox("Sort", ["Priority","Difficulty","Time","Status"],
                                   label_visibility="collapsed")
        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

        day_labels = []
        for i, (ds, df) in enumerate(zip(days_short, DAYS_FULL)):
            cnt    = len(st.session_state.week_instance.days[i].tasks)
            dot    = "● " if df == today_name else ""
            suffix = f"·{cnt}" if cnt else ""
            day_labels.append(f"{dot}{ds}{suffix}")

        day_tabs = st.tabs(day_labels)

        for i, (d_short, d_full) in enumerate(zip(days_short, DAYS_FULL)):
            day_obj = st.session_state.week_instance.days[i]
            with day_tabs[i]:
                tasks = list(day_obj.tasks)
                if sf:
                    tasks = [t for t in tasks if sf in t.taskName.lower()]

                if sort_choice == "Priority":     tasks.sort(key=lambda x: x.priority, reverse=True)
                elif sort_choice == "Difficulty": tasks.sort(key=lambda x: x.taskDifficulty, reverse=True)
                elif sort_choice == "Time":       tasks.sort(key=lambda x: x.timeStart)
                elif sort_choice == "Status":     tasks.sort(key=lambda x: x.getProgress())

                if not tasks:
                    st.markdown('<div style="color:#333;font-size:10px;padding:8px 0;">— empty —</div>', unsafe_allow_html=True)
                else:
                    last_cat = None
                    for t in tasks:
                        # Category header
                        cat = None
                        if sort_choice == "Priority":
                            cat = "HIGH" if t.priority >= 80 else ("MID" if t.priority >= 55 else "LOW")
                        elif sort_choice == "Status":
                            p   = t.getProgress()
                            cat = "DONE" if p == 100 else ("IN PROGRESS" if p > 0 else "TODO")
                        if cat and cat != last_cat:
                            st.markdown(f'<div class="label-text" style="margin-top:8px;">{cat}</div>', unsafe_allow_html=True)
                            last_cat = cat

                        tag     = EVENT_TAGS.get(t.eventTag, "Task")
                        col     = TYPE_COLORS.get(tag, "#fff")
                        prog    = t.getProgress()
                        t_str   = mins_to_time(t.timeStart).strftime("%H:%M")
                        is_sel  = st.session_state.selected_task_id == t.id
                        cd      = countdown_label(t, d_full)
                        prog_c  = "#0f0" if prog == 100 else ("#ff0" if prog > 0 else "#1a1a1a")

                        # Coloured left-border strip
                        st.markdown(
                            f'<div style="height:1px;background:linear-gradient(to right,{col}22,transparent);margin-bottom:2px;"></div>',
                            unsafe_allow_html=True
                        )

                        rc1, rc2 = st.columns([7, 1])
                        with rc1:
                            label = f"{'▷' if is_sel else '▶'} [{t_str}] {t.taskName}"
                            if st.button(label, key=f"sel_{t.id}", use_container_width=True):
                                st.session_state.selected_task_id = None if is_sel else t.id
                                st.rerun()
                        with rc2:
                            if prog == 100:
                                st.markdown('<span class="task-status-badge status-done" style="font-size:7px;">✓</span>', unsafe_allow_html=True)
                            elif prog > 0:
                                st.markdown(f'<span class="task-status-badge status-progress" style="font-size:7px;">{prog:.0f}%</span>', unsafe_allow_html=True)
                            else:
                                st.markdown(f'<span style="font-size:7px;color:{col};">{tag[:3].upper()}</span>', unsafe_allow_html=True)

                        # Mini progress bar + countdown
                        st.markdown(
                            f'<div style="display:flex;align-items:center;gap:8px;margin-top:-6px;margin-bottom:4px;">'
                            f'<div style="flex:1;height:2px;background:#111;">'
                            f'<div style="height:2px;background:{prog_c};width:{max(int(prog),0)}%;"></div></div>'
                            f'{cd}</div>',
                            unsafe_allow_html=True
                        )

                st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

                # Template picker + add button
                tpls = list(st.session_state.task_templates.keys())
                if tpls:
                    ta1, ta2 = st.columns([3, 2])
                    with ta1:
                        chosen_tpl = st.selectbox("Template", ["--"] + tpls,
                                                  key=f"tpl_pick_{d_full}", label_visibility="collapsed")
                    with ta2:
                        if st.button(f"+ ADD TO {d_short}", key=f"add_{d_full}", use_container_width=True):
                            tpl = st.session_state.task_templates.get(chosen_tpl) if chosen_tpl != "--" else None
                            add_new_task(day_obj, tpl)
                            st.rerun()
                else:
                    if st.button(f"+ ADD TO {d_short}", key=f"add_{d_full}", use_container_width=True):
                        add_new_task(day_obj)
                        st.rerun()

    with right_col:
        if st.session_state.selected_task_id:
            selected_task = None
            for day in st.session_state.week_instance.days:
                for t in day.tasks:
                    if t.id == st.session_state.selected_task_id:
                        selected_task = t; break
                if selected_task: break
            if selected_task:
                render_task_detail(selected_task)
            else:
                st.session_state.selected_task_id = None
        else:
            st.markdown(
                '<div style="color:#222;font-size:10px;padding-top:4rem;text-align:center;">'
                '— select a task to edit —</div>',
                unsafe_allow_html=True
            )


elif st.session_state.current_view == 'timetable':
    st.markdown("### TIMETABLE")
    st.markdown('<div class="label-text">Chronological view — all tasks this week</div>', unsafe_allow_html=True)
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    today_name  = datetime.now().strftime("%A")
    active_days = [d.name for d in st.session_state.week_instance.days if d.tasks]

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
                today_badge  = '&nbsp;<span style="color:#0f0;font-size:8px;">● TODAY</span>' if is_today else ""
                st.markdown(
                    f'<div style="font-size:9px;color:#555;margin-bottom:10px;">'
                    f'{len(sorted_tasks)} tasks · {th}h {tm:02d}m total{today_badge}</div>',
                    unsafe_allow_html=True
                )
                for task in sorted_tasks:
                    start_str  = mins_to_time(task.timeStart).strftime("%H:%M")
                    end_str    = mins_to_time(task.timeEnd).strftime("%H:%M")
                    dur_h      = task.taskDuration // 60
                    dur_m      = task.taskDuration % 60
                    dur_str    = f"{dur_h}h {dur_m}m" if dur_h else f"{dur_m}m"
                    progress   = task.getProgress()
                    bar_w      = max(int(progress), 2)
                    bar_color  = "#0f0" if progress == 100 else ("#ff0" if progress > 0 else "#222")
                    tag        = EVENT_TAGS.get(task.eventTag, "Task")
                    name_color = TYPE_COLORS.get(tag, "#fff")
                    n_subs     = len(task.subTasks)
                    done_subs  = sum(1 for s in task.subTasks if s.status)
                    sub_str    = f"{done_subs}/{n_subs} subtasks" if n_subs else "no subtasks"
                    cd         = countdown_label(task, day_name)

                    c1, c2, c3 = st.columns([2, 5, 2])
                    with c1:
                        st.markdown(
                            f'<div style="font-size:9px;color:#555;padding-top:4px;">'
                            f'{start_str}<br/>{end_str}</div>',
                            unsafe_allow_html=True
                        )
                    with c2:
                        st.markdown(
                            f'<div style="font-size:11px;color:{name_color};margin-bottom:4px;">'
                            f'{task.taskName} {cd}</div>'
                            f'<div style="height:2px;background:#111;">'
                            f'<div style="height:2px;background:{bar_color};width:{bar_w}%;"></div></div>'
                            f'<div style="font-size:8px;color:#444;margin-top:3px;">{tag} · {sub_str}</div>',
                            unsafe_allow_html=True
                        )
                    with c3:
                        pct_col = "#0f0" if progress == 100 else ("#ff0" if progress > 0 else "#444")
                        st.markdown(
                            f'<div style="font-size:9px;color:#555;text-align:right;padding-top:4px;">'
                            f'{dur_str}<br/><span style="color:{pct_col};">{progress:.0f}%</span></div>',
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
                if not url.startswith("http"): url = "https://" + url
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
        notes = st.text_area("", height=440, value=st.session_state.handbook_notes,
                             key="notepad", label_visibility="collapsed")
        if notes != st.session_state.handbook_notes:
            st.session_state.handbook_notes = notes
            fn.save_handbook_notes(notes)


elif st.session_state.current_view == 'progress':
    tasks      = [t for d in st.session_state.week_instance.days for t in d.tasks]
    total_subs = sum(len(t.subTasks) for t in tasks)
    done_subs  = sum(sum(1 for s in t.subTasks if s.status) for t in tasks)
    prog_pct   = (done_subs / total_subs * 100) if total_subs > 0 else 0

    st.markdown("### PRODUCTIVITY OVERVIEW")
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # Overall bar
    st.progress(prog_pct / 100)
    st.markdown(
        f'<div style="font-size:10px;color:#555;margin:4px 0 16px;">'
        f'{done_subs}/{total_subs} subtasks · {prog_pct:.1f}% complete</div>',
        unsafe_allow_html=True
    )

    # ── Heatmap ──
    st.markdown('<div class="label-text">Weekly Load Heatmap</div>', unsafe_allow_html=True)
    hm_cols = st.columns(7)
    today_name = datetime.now().strftime("%A")
    max_dur = 1
    day_data = []
    for day_obj in st.session_state.week_instance.days:
        dur   = sum(t.taskDuration for t in day_obj.tasks)
        cnt   = len(day_obj.tasks)
        dpct  = (sum(sum(1 for s in t.subTasks if s.status) for t in day_obj.tasks) /
                 max(sum(len(t.subTasks) for t in day_obj.tasks), 1) * 100)
        day_data.append((day_obj.name, dur, cnt, dpct))
        if dur > max_dur: max_dur = dur

    for col, (dname, dur, cnt, dpct) in zip(hm_cols, day_data):
        with col:
            intensity = dur / max_dur if max_dur else 0
            r = int(255 * intensity * 0.6)
            g = int(255 * intensity * 0.9)
            b = int(255 * intensity * 0.4)
            bg    = f"#{r:02x}{g:02x}{b:02x}" if dur > 0 else "#0a0a0a"
            today_mark = "●" if dname == today_name else ""
            h, m  = dur // 60, dur % 60
            dur_s = f"{h}h{m:02d}" if dur else "—"
            st.markdown(
                f'<div style="background:{bg};padding:8px 4px;text-align:center;'
                f'border:1px solid #1a1a1a;">'
                f'<div style="font-size:9px;color:{"#fff" if dur>0 else "#333"};letter-spacing:0.1em;">'
                f'{today_mark}{dname[:3].upper()}</div>'
                f'<div style="font-size:11px;color:{"#fff" if dur>0 else "#222"};margin:4px 0;">'
                f'{cnt}</div>'
                f'<div style="font-size:8px;color:{"#aaa" if dur>0 else "#222"};">{dur_s}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # ── In Progress + Completed ──
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="label-text">In Progress</div>', unsafe_allow_html=True)
        in_prog = [t for t in tasks if 0 < sum(1 for s in t.subTasks if s.status) < len(t.subTasks)]
        if not in_prog:
            st.markdown('<div style="color:#333;font-size:10px;">None</div>', unsafe_allow_html=True)
        for t in in_prog:
            p   = t.getProgress()
            tag = EVENT_TAGS.get(t.eventTag, "Task")
            col = TYPE_COLORS.get(tag, "#fff")
            st.markdown(
                f'<div style="font-size:10px;margin-bottom:6px;">'
                f'<span style="color:{col};">▌</span> {t.taskName}'
                f'<span style="color:#ff0;font-size:8px;margin-left:6px;">{p:.0f}%</span>'
                f'<div style="height:2px;background:#111;margin-top:2px;">'
                f'<div style="height:2px;background:#ff0;width:{int(p)}%;"></div></div></div>',
                unsafe_allow_html=True
            )
    with c2:
        st.markdown('<div class="label-text">Completed</div>', unsafe_allow_html=True)
        completed = [t for t in tasks if t.subTasks and all(s.status for s in t.subTasks)]
        if not completed:
            st.markdown('<div style="color:#333;font-size:10px;">None</div>', unsafe_allow_html=True)
        for t in completed:
            st.markdown(
                f'<div style="font-size:10px;color:#0f0;margin-bottom:4px;">✓ {t.taskName}</div>',
                unsafe_allow_html=True
            )

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # ── Per-day breakdown ──
    st.markdown('<div class="label-text">By Day</div>', unsafe_allow_html=True)
    for day_obj in st.session_state.week_instance.days:
        day_tasks = day_obj.tasks
        if not day_tasks: continue
        day_subs = sum(len(t.subTasks) for t in day_tasks)
        day_done = sum(sum(1 for s in t.subTasks if s.status) for t in day_tasks)
        day_pct  = (day_done / day_subs * 100) if day_subs > 0 else 0
        bar_col  = "#0f0" if day_pct == 100 else ("#ff0" if day_pct > 0 else "#333")
        is_today = day_obj.name == today_name
        today_m  = " ●" if is_today else ""
        st.markdown(
            f'<div style="display:flex;justify-content:space-between;font-size:9px;color:#555;margin-bottom:2px;">'
            f'<span>{day_obj.name[:3].upper()}{today_m}</span>'
            f'<span>{len(day_tasks)} tasks · {day_done}/{day_subs} · {day_pct:.0f}%</span></div>'
            f'<div style="height:2px;background:#111;margin-bottom:6px;">'
            f'<div style="height:2px;background:{bar_col};width:{int(day_pct)}%;"></div></div>',
            unsafe_allow_html=True
        )
