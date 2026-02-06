class subTask:
    def __init__(self, name="Subtask", status=False):
        self.name = name
        self.status = status

    def markDone(self):
        self.status = True

    def markUndone(self):
        self.status = False


class Task:
    def __init__(self):
        self.taskName = "Task"
        self.taskDifficulty = 3
        self.taskDeadline = 1
        self.timeStart = 0
        self.timeEnd = 0
        self.taskDuration = 0
        self.eventTag = 3
        self.timeFrame = 2
        self.taskRecurrence = 1
        self.subTasks = []
        self.priority = 0
        self.day = "Monday"
        self.durationCategory = "Moment"
        self.remainingDays = 0

    def updateDuration(self):
        self.taskDuration = max(self.timeEnd - self.timeStart, 0)
        if self.taskDuration <= 30:
            self.durationCategory = "Moment"
        elif self.taskDuration <= 90:
            self.durationCategory = "???"
        else:
            self.durationCategory = "Session"

    def addSubTask(self, subtask):
        if isinstance(subtask, subTask):
            self.subTasks.append(subtask)
        else:
            raise TypeError("Must add subTask object")

    def removeSubTask(self, subtask):
        if subtask in self.subTasks:
            self.subTasks.remove(subtask)

    def getProgress(self):
        if not self.subTasks:
            return 0
        done = sum(1 for s in self.subTasks if s.status)
        return round((done / len(self.subTasks)) * 100, 1)

    def setValue(self, aspect, value):
        if hasattr(self, aspect):
            setattr(self, aspect, value)
            if aspect in ("timeStart", "timeEnd"):
                self.updateDuration()
        else:
            raise AttributeError(f"Task has no attribute '{aspect}'")

    def getValue(self, aspect):
        if hasattr(self, aspect):
            return getattr(self, aspect)
        else:
            raise AttributeError(f"Task has no attribute '{aspect}'")

    def setPriority(self):
        self.updateDuration()
        recurrence = max(self.taskRecurrence, 1)
        timeframe = max(self.timeFrame, 1)
        sub_count = max(len(self.subTasks), 1)
        effort = (self.taskDifficulty * self.eventTag) / recurrence
        load = (self.taskDuration / sub_count) / timeframe
        urgency = 1 + (self.taskDeadline * 0.3)
        raw = (effort + load) * urgency
        self.priority = round(100 * (raw / (raw + 10)), 2)


class Bundle:
    def __init__(self):
        self.tasks = []
        self.recurrence = 0

    def updateRecurrence(self):
        self.recurrence = len(self.tasks)

    def addTask(self, task):
        if isinstance(task, Task):
            self.tasks.append(task)
            self.updateRecurrence()
        else:
            raise TypeError("Only Task objects allowed")

    def deleteTask(self, task):
        if task in self.tasks:
            self.tasks.remove(task)
            self.updateRecurrence()
        else:
            raise ValueError("Task not found in bundle")

    def edit(self, task, aspect, value):
        if task in self.tasks:
            task.setValue(aspect, value)
            self.updateRecurrence()
        else:
            raise ValueError("Task not found in bundle")

    def sortByTask(self):
        self.tasks.sort(key=lambda t: t.eventTag, reverse=True)


class Day:
    def __init__(self, name="???"):
        self.name = name
        self.tasks = []
        self.Event = []
        self.Assignment = []
        self.Tasks = []
        self.Chores = []
        self.sortedPriority = []
        self.sortedDifficulty = []
        self.sortedTime = []
        self.highPriority = []
        self.mediumPriority = []
        self.smallPriority = []

    def addTask(self, task):
        if isinstance(task, Task):
            self.tasks.append(task)
        else:
            raise TypeError("Only Task objects allowed")

    def removeTask(self, task):
        if task in self.tasks:
            self.tasks.remove(task)

    def organizeTasks(self):
        self.Event = []
        self.Assignment = []
        self.Tasks = []
        self.Chores = []
        for t in self.tasks:
            t.setPriority()
            t.updateDuration()
            t.remainingDays = max(t.taskDeadline, 0)
            if t.eventTag == 5:
                self.Event.append(t)
            elif t.eventTag == 4:
                self.Assignment.append(t)
            elif t.eventTag == 3:
                self.Tasks.append(t)
            elif t.eventTag == 1:
                self.Chores.append(t)
        self.Event.sort(key=lambda t: t.priority, reverse=True)
        self.Assignment.sort(key=lambda t: t.priority, reverse=True)
        self.Tasks.sort(key=lambda t: t.priority, reverse=True)
        self.Chores.sort(key=lambda t: t.priority, reverse=True)
        self.tasks = self.Event + self.Assignment + self.Tasks + self.Chores
        self.highPriority = []
        self.mediumPriority = []
        self.smallPriority = []
        for t in self.tasks:
            if t.priority >= 80 and len(self.highPriority) < 3:
                self.highPriority.append(t)
            elif t.priority >= 70 and len(self.mediumPriority) < 4:
                self.mediumPriority.append(t)
            else:
                self.smallPriority.append(t)


class week:
    def __init__(self):
        self.Monday = Day("Monday")
        self.Tuesday = Day("Tuesday")
        self.Wednesday = Day("Wednesday")
        self.Thursday = Day("Thursday")
        self.Friday = Day("Friday")
        self.Saturday = Day("Saturday")
        self.Sunday = Day("Sunday")
        self.days = [
            self.Monday,
            self.Tuesday,
            self.Wednesday,
            self.Thursday,
            self.Friday,
            self.Saturday,
            self.Sunday
        ]

    def addTaskToDay(self, task, day_name):
        for d in self.days:
            if d.name == day_name:
                d.addTask(task)
                return
        raise ValueError(f"No day named '{day_name}' in week")

    def organizeWeek(self):
        for d in self.days:
            d.organizeTasks()

    def insertBundle(self, bundle):
        for task in bundle.tasks:
            day_name = getattr(task, "day", None)
            if day_name:
                self.addTaskToDay(task, day_name)
        self.organizeWeek()
