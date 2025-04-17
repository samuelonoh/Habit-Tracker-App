from datetime import datetime, timezone, time, timedelta
import pytest

@pytest.fixture
def daily_completions():
    """
    Generate 28 days of consecutive completion timestamps,
    ending at today’s midnight in UTC, for testing daily streaks.
    """
    today = datetime.now(timezone.utc).date()
    return [
        datetime.combine(today - timedelta(days=i), time(), tzinfo=timezone.utc)
        for i in range(28)
    ]

@pytest.fixture
def weekly_completions():
    """
    Generate 4 weekly completions, spaced exactly 7 days apart,
    ending at today’s midnight in UTC, for testing weekly streaks.
    """
    today = datetime.now(timezone.utc).date()
    return [
        datetime.combine(today - timedelta(weeks=i), time(), tzinfo=timezone.utc)
        for i in range(4)
    ]
