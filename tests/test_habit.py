import datetime
import tempfile
import pytest
from src.persistence import DatabaseAdapter
from src.models import HabitTracker
from src.analytics import calculate_streak, longest_streak_all, longest_streak_for

def test_habit_lifecycle(tmp_path):
    # Set up a fresh database in a temp file
    db_file = tmp_path / "test.db"
    adapter = DatabaseAdapter(str(db_file))
    tracker = HabitTracker(adapter)

    # Create a new daily habit
    habit = tracker.add_habit("Test Habit", "daily")
    assert habit.id is not None

    # Initially no completions -> streak zero
    assert calculate_streak([], "daily") == 0

    # Mark completion now
    tracker.complete_habit(habit.id)
    completions = adapter.load_completions(habit.id)
    assert len(completions) == 1
    assert calculate_streak(completions, "daily") == 1

    # Add yesterday’s completion to build a 2‑day streak
    yesterday = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=1)
    tracker.complete_habit(habit.id, when=yesterday)
    completions = adapter.load_completions(habit.id)
    assert calculate_streak(completions, "daily") == 2

def test_daily_and_weekly_streaks(daily_completions, weekly_completions):
    # 28 consecutive days => streak 28
    assert calculate_streak(daily_completions, "daily") == 28

    # 4 consecutive weeks => streak 4
    assert calculate_streak(weekly_completions, "weekly") == 4

def test_longest_streak_helpers(daily_completions):
    # Create two in‑memory Habit objects for testing analytics
    from src.models import Habit
    h1 = Habit("H1", "daily"); h1.id = 1; h1.completions = daily_completions
    h2 = Habit("H2", "daily"); h2.id = 2; h2.completions = daily_completions[:-5]

    all_streaks = longest_streak_all([h1, h2])
    assert all_streaks == {1: 28, 2: 23}
    assert longest_streak_for(h2) == 23



