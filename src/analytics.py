import datetime
from typing import List, Dict


def filter_by_periodicity(habits: List, periodicity: str) -> List:
    return [h for h in habits if h.periodicity == periodicity]


def calculate_streak(completions: List[datetime.datetime], periodicity: str) -> int:
    if not completions:
        return 0
    dates = sorted({c.date() for c in completions})
    streak = 1
    for prev, curr in zip(dates[::-1][1:], dates[::-1]):
        diff = curr - prev
        if (periodicity == 'daily' and diff == datetime.timedelta(days=1)) or \
           (periodicity == 'weekly' and datetime.timedelta(days=7) <= diff < datetime.timedelta(days=14)):
            streak += 1
        else:
            break
    return streak


def longest_streak_all(habits: List) -> Dict[int, int]:
    return {h.id: calculate_streak(h.completions, h.periodicity) for h in habits}


def longest_streak_for(habit) -> int:
    return calculate_streak(habit.completions, habit.periodicity)