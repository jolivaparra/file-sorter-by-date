from datetime import datetime
from pathlib import Path
import random


def valid_date(year, month, day, hour=0, minute=0, second=0):
    """Checks if a generated date is valid (e.g., avoids February 30th)."""
    try:
        datetime(year, month, day, hour, minute, second)
        return True
    except ValueError:
        return False


def generate_test_data():
    """Generates dummy files with random timestamps in the 'test/source' folder."""
    root = Path("test")
    des = root / "source"
    des.mkdir(parents=True, exist_ok=True)

    count = 0

    years = [2020, 2021, 2022, 2023, 2024, 2025]
    weights_years = [1, 2, 3, 10, 15, 5]

    months = list(range(1, 13))
    weights_months = [10, 10] + [1] * (12 - 2)

    days = range(1, 32)
    weights_days = ([1] * 5 + [10] * 2) * 4 + [1] * 3

    while count < 300:
        year = random.choices(years, weights=weights_years, k=1)[0]
        month = random.choices(months, weights=weights_months, k=1)[0]
        day = random.choices(days, weights=weights_days, k=1)[0]

        hour = random.randint(0, 23)
        minute = random.randint(0, 59)
        second = random.randint(0, 59)

        if valid_date(year, month, day, hour, minute, second):
            file_name = (
                f"{year}{month:02d}{day:02d}_{hour:02d}{minute:02d}{second:02d}.txt"
            )
            (des / file_name).touch()
            count += 1


if __name__ == "__main__":
    generate_test_data()
