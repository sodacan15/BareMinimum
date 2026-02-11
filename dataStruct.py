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
        self.timeStart = 540 # 9:00 AM
        self.timeEnd = 600   # 10:00 AM
        self.taskDuration = 60
        self.eventTag = 3
        self.timeFrame = 2
        self.taskRecurrence = 1
        self.subTasks = []
        self.priority = 0
        self.day = "Monday"

    def clone(self):
        new_t = Task()
        # Use a dictionary to ensure we aren't dragging old references
        new_t.taskName = str(self.taskName)
        new_t.taskDifficulty = int(self.taskDifficulty)
        new_t.taskDeadline = int(self.taskDeadline)
        new_t.timeStart = int(self.timeStart)
        new_t.timeEnd = int(self.timeEnd)
        new_t.eventTag = int(self.eventTag)
        new_t.timeFrame = int(self.timeFrame)
        new_t.day = str(self.day)
        
        # CLEAR and REBUILD subtasks from scratch
        new_t.subTasks = []
        for st in self.subTasks:
            # Create a brand new object with a brand new UUID
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
        """
        IMPROVED PRIORITY SCORING SYSTEM
        
        Components:
        1. Deadline Weight (0-40 points): Hard deadlines get massive priority
        2. Difficulty Score (0-25 points): Task complexity matters
        3. Time Investment (0-20 points): Longer tasks need planning
        4. Task Type Weight (0-15 points): Important event types prioritized
        5. Subtask Complexity (0-10 points): More subtasks = more planning needed
        6. Recurrence Bonus (0-10 points): Recurring tasks get slight boost (habit forming)
        
        Total: 0-120 points (normalized to 0-100%)
        """
        self.updateDuration()
        
        # 1. DEADLINE WEIGHT (0-40 points) - Most important factor
        if self.taskDeadline == 1:  # Hard deadline
            deadline_score = 40
        else:  # Soft deadline
            deadline_score = 15
        
        # 2. DIFFICULTY SCORE (0-25 points)
        # Scale: 1=5pts, 2=10pts, 3=15pts, 4=20pts, 5=25pts
        difficulty_score = self.taskDifficulty * 5
        
        # 3. TIME INVESTMENT (0-20 points)
        # Normalize duration: 0-2hrs=5pts, 2-4hrs=10pts, 4-6hrs=15pts, 6+hrs=20pts
        hours = self.taskDuration / 60
        if hours < 2:
            time_score = 5
        elif hours < 4:
            time_score = 10
        elif hours < 6:
            time_score = 15
        else:
            time_score = 20
        
        # 4. TASK TYPE WEIGHT (0-15 points)
        # Event=15, Assignment=12, Task=8, Chore=4
        type_weights = {5: 15, 4: 12, 3: 8, 1: 4}
        type_score = type_weights.get(self.eventTag, 8)
        
        # 5. SUBTASK COMPLEXITY (0-10 points)
        # More subtasks = more coordination needed
        subtask_count = len(self.subTasks)
        if subtask_count <= 2:
            subtask_score = 3
        elif subtask_count <= 5:
            subtask_score = 6
        elif subtask_count <= 8:
            subtask_score = 8
        else:
            subtask_score = 10
        
        # 6. RECURRENCE BONUS (0-10 points)
        # Recurring tasks get a small boost (building habits is important)
        if self.taskRecurrence > 1:
            recurrence_score = min(10, 2 + (self.taskRecurrence * 1.5))
        else:
            recurrence_score = 0
        
        # TOTAL SCORE (max 120 points)
        raw_score = (
            deadline_score + 
            difficulty_score + 
            time_score + 
            type_score + 
            subtask_score + 
            recurrence_score
        )
        
        # Normalize to 0-100 scale
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
        """
        Sorts tasks and categorizes them with improved thresholds.
        
        Priority Categories (based on score):
        - HIGH (80-100%): Critical tasks requiring immediate attention - Narrower range for focus
        - MEDIUM (55-79%): Important tasks to tackle after high priority - Moderate range
        - LOW (0-54%): Tasks that can be deferred if needed - Widest range for flexibility
        
        Position-based limits:
        - Top 2-3 tasks → High Priority (regardless of score if >= 55)
        - Next 3-4 tasks → Medium Priority
        - Rest → Low Priority
        """
        for t in self.tasks: t.setPriority()
        # Sort by priority score (highest first)
        self.tasks.sort(key=lambda x: x.priority, reverse=True)
        
        # Clear previous categorization
        self.highPriority = []
        self.mediumPriority = []
        self.smallPriority = []
        
        # HYBRID APPROACH: Use both score thresholds AND position limits
        
        # Wider ranges as priority decreases: HIGH=20pts, MEDIUM=25pts, LOW=55pts
        high_threshold = 80
        medium_threshold = 55
        
        for task in self.tasks:
            if task.priority >= high_threshold:
                self.highPriority.append(task)
            elif task.priority >= medium_threshold:
                self.mediumPriority.append(task)
            else:
                self.smallPriority.append(task)
        
        # Second pass: Enforce position-based limits (max 3 high, max 4 medium)
        # If we have too many high priority tasks, demote extras to medium
        if len(self.highPriority) > 3:
            overflow = self.highPriority[3:]
            self.highPriority = self.highPriority[:3]
            self.mediumPriority = overflow + self.mediumPriority
        
        # If we have too many medium priority tasks, demote extras to low
        if len(self.mediumPriority) > 4:
            overflow = self.mediumPriority[4:]
            self.mediumPriority = self.mediumPriority[:4]
            self.smallPriority = overflow + self.smallPriority
        
        # Edge case: If we have fewer than 3 tasks total but they're all low priority,
        # promote the top ones to ensure we always have some focus areas
        if len(self.tasks) > 0 and len(self.highPriority) == 0:
            # Promote top task to high if its score is at least 45
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
        # Update recurrence counts globally
        all_task_names = [t.taskName for d in self.days for t in d.tasks]
        for d in self.days:
            for t in d.tasks:
                t.taskRecurrence = all_task_names.count(t.taskName)
            d.organizeTasks()
