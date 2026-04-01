import uuid

class subTask:
    def __init__(self, name="Subtask", status=False):
        self.id = str(uuid.uuid4())
        self.name = name
        self.status = status

    def markDone(self): self.status = True
    def markUndone(self): self.status = False

class Task:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.taskName = "Task"
        self.taskDifficulty = 3
        self.taskDeadline = 1
        self.timeStart = 540
        self.timeEnd = 600
        self.taskDuration = 60
        self.eventTag = 3
        self.timeFrame = 2
        self.taskRecurrence = 1
        self.subTasks = []
        self.priority = 0
        self.day = "Monday"

    def clone(self):
        new_t = Task()
        new_t.taskName = str(self.taskName)
        new_t.taskDifficulty = int(self.taskDifficulty)
        new_t.taskDeadline = int(self.taskDeadline)
        new_t.timeStart = int(self.timeStart)
        new_t.timeEnd = int(self.timeEnd)
        new_t.eventTag = int(self.eventTag)
        new_t.timeFrame = int(self.timeFrame)
        new_t.day = str(self.day)
        new_t.subTasks = []
        for st in self.subTasks:
            new_t.subTasks.append(subTask(name=str(st.name), status=bool(st.status)))
        new_t.setPriority()
        return new_t

    def updateDuration(self):
        if self.timeEnd >= self.timeStart:
            self.taskDuration = self.timeEnd - self.timeStart
        else:
            self.taskDuration = (1440 - self.timeStart) + self.timeEnd

    def addSubTask(self, subtask):
        self.subTasks.append(subtask)

    def removeSubTask(self, sub_obj):
        self.subTasks = [s for s in self.subTasks if s.id != sub_obj.id]

    def getProgress(self):
        if not self.subTasks: return 0
        done = sum(1 for s in self.subTasks if s.status)
        return round((done / len(self.subTasks)) * 100, 1)

    def setValue(self, aspect, value):
        if hasattr(self, aspect):
            setattr(self, aspect, value)
            if aspect in ("timeStart", "timeEnd"): self.updateDuration()

    def setPriority(self):
        self.updateDuration()

        if self.taskDeadline == 1:
            deadline_score = 40
        else:
            deadline_score = 15

        difficulty_score = self.taskDifficulty * 5

        hours = self.taskDuration / 60
        if hours < 2:
            time_score = 5
        elif hours < 4:
            time_score = 10
        elif hours < 6:
            time_score = 15
        else:
            time_score = 20

        type_weights = {5: 15, 4: 12, 3: 8, 1: 4}
        type_score = type_weights.get(self.eventTag, 8)

        subtask_count = len(self.subTasks)
        if subtask_count <= 2:
            subtask_score = 3
        elif subtask_count <= 5:
            subtask_score = 6
        elif subtask_count <= 8:
            subtask_score = 8
        else:
            subtask_score = 10

        if self.taskRecurrence > 1:
            recurrence_score = min(10, 2 + (self.taskRecurrence * 1.5))
        else:
            recurrence_score = 0

        raw_score = (
            deadline_score +
            difficulty_score +
            time_score +
            type_score +
            subtask_score +
            recurrence_score
        )

        self.priority = round(min(100, (raw_score / 120) * 100), 2)


class Day:
    def __init__(self, name):
        self.id = str(uuid.uuid4())
        self.name = name
        self.tasks = []
        self.highPriority = []
        self.mediumPriority = []
        self.smallPriority = []

    def addTask(self, task):
        task.day = self.name
        self.tasks.append(task)

    def removeTask(self, task_obj):
        self.tasks = [t for t in self.tasks if t.id != task_obj.id]

    def organizeTasks(self):
        for t in self.tasks: t.setPriority()
        self.tasks.sort(key=lambda x: x.priority, reverse=True)

        self.highPriority = []
        self.mediumPriority = []
        self.smallPriority = []

        high_threshold = 80
        medium_threshold = 55

        for task in self.tasks:
            if task.priority >= high_threshold:
                self.highPriority.append(task)
            elif task.priority >= medium_threshold:
                self.mediumPriority.append(task)
            else:
                self.smallPriority.append(task)

        if len(self.highPriority) > 3:
            overflow = self.highPriority[3:]
            self.highPriority = self.highPriority[:3]
            self.mediumPriority = overflow + self.mediumPriority

        if len(self.mediumPriority) > 4:
            overflow = self.mediumPriority[4:]
            self.mediumPriority = self.mediumPriority[:4]
            self.smallPriority = overflow + self.smallPriority

        if len(self.tasks) > 0 and len(self.highPriority) == 0:
            if self.tasks[0].priority >= 45:
                self.highPriority = [self.tasks[0]]
                self.mediumPriority = [t for t in self.mediumPriority if t.id != self.tasks[0].id]
                self.smallPriority = [t for t in self.smallPriority if t.id != self.tasks[0].id]


class week:
    def __init__(self):
        self.days = [Day(n) for n in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]]
        self.Monday, self.Tuesday, self.Wednesday, self.Thursday, self.Friday, self.Saturday, self.Sunday = self.days

    def addTaskToDay(self, task, day_name):
        for d in self.days:
            if d.name == day_name: d.addTask(task)

    def organizeWeek(self):
        all_task_names = [t.taskName for d in self.days for t in d.tasks]
        for d in self.days:
            for t in d.tasks:
                t.taskRecurrence = all_task_names.count(t.taskName)
            d.organizeTasks()
