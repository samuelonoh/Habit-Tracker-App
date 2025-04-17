import datetime
from typing import List, Optional

class Habit:
    """
    A habit with a name, periodicity, and completion log.
    """
    def __init__(self, name: str, periodicity: str):
        self.id: Optional[int] = None
        self.name = name
        self.periodicity = periodicity  # 'daily' or 'weekly'
        self.created_at = datetime.datetime.now(datetime.timezone.utc)
        self.completions: List[datetime.datetime] = []

    def complete(self, when: Optional[datetime.datetime] = None):
        """Mark as completed at UTC timestamp."""
        ts = when or datetime.datetime.now(datetime.timezone.utc)
        self.completions.append(ts)

    def __repr__(self):
        return f"<Habit {self.id}: {self.name} ({self.periodicity})>"


class HabitTracker:
    """
    Manages creation, deletion, listing, and completion of habits.
    """
    def __init__(self, db_adapter):
        self.db = db_adapter
        self.habits = {}
        for h in self.db.load_all_habits():
            h.completions = self.db.load_completions(h.id)
            self.habits[h.id] = h

    def add_habit(self, name: str, periodicity: str) -> Habit:
        habit = Habit(name, periodicity)
        habit.id = self.db.insert_habit(habit)
        self.habits[habit.id] = habit
        return habit

    def delete_habit(self, habit_id: int):
        self.db.delete_habit(habit_id)
        self.habits.pop(habit_id, None)

    def list_habits(self, periodicity: Optional[str] = None):
        habits = list(self.habits.values())
        return [h for h in habits if not periodicity or h.periodicity == periodicity]

    def complete_habit(self, habit_id: int, when: Optional[datetime.datetime] = None):
        habit = self.habits[habit_id]
        habit.complete(when)
        self.db.insert_completion(habit_id, habit.completions[-1])

    def get_completions(self, habit_id: int):
        return self.db.load_completions(habit_id)