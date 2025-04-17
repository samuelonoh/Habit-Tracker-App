import os
import sqlite3
import datetime
from typing import List
from .models import Habit

DB_PATH = "data/habits.db"

class DatabaseAdapter:
    """
    SQLite adapter for habits and completions.
    """
    def __init__(self, db_path=DB_PATH):
        # Ensure parent directory exists
        parent = os.path.dirname(db_path)
        if parent and not os.path.exists(parent):
            os.makedirs(parent, exist_ok=True)  # create data/ if missing
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._migrate()

    def _migrate(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS habits (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    periodicity TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )""")
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS completions (
                    id INTEGER PRIMARY KEY,
                    habit_id INTEGER,
                    timestamp TEXT NOT NULL,
                    FOREIGN KEY(habit_id) REFERENCES habits(id)
                )""")

    def insert_habit(self, habit: Habit) -> int:
        cur = self.conn.execute(
            "INSERT INTO habits (name, periodicity, created_at) VALUES (?,?,?)",
            (habit.name, habit.periodicity, habit.created_at.isoformat())
        )
        self.conn.commit()
        return cur.lastrowid

    def load_all_habits(self) -> List[Habit]:
        rows = self.conn.execute("SELECT * FROM habits").fetchall()
        habits = []
        for r in rows:
            h = Habit(r["name"], r["periodicity"])
            h.id = r["id"]
            h.created_at = datetime.datetime.fromisoformat(r["created_at"])
            habits.append(h)
        return habits

    def delete_habit(self, habit_id: int):
        with self.conn:
            self.conn.execute("DELETE FROM completions WHERE habit_id=?", (habit_id,))
            self.conn.execute("DELETE FROM habits WHERE id=?", (habit_id,))

    def insert_completion(self, habit_id: int, when: datetime.datetime):
        self.conn.execute(
            "INSERT INTO completions (habit_id, timestamp) VALUES (?,?)",
            (habit_id, when.isoformat())
        )
        self.conn.commit()

    def load_completions(self, habit_id: int) -> List[datetime.datetime]:
        rows = self.conn.execute(
            "SELECT timestamp FROM completions WHERE habit_id=? ORDER BY timestamp",
            (habit_id,)
        ).fetchall()
        return [datetime.datetime.fromisoformat(r["timestamp"]) for r in rows]