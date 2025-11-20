import datetime
from projman.src.domain.free_range import FreeRange

class WorkingDayRepository:
    def __init__(self) -> None:
        self.free_weekdays = set()
        self.free_ranges = []

    # takes Weekdays as arguments
    def set_free_weekdays(self, *args) -> None:
        for weekday in args:
            self.free_weekdays.add(weekday)

    def add_free_range(self, firstFreeDay: datetime.date, lastFreeDay: datetime.date, description: str = "") -> None:
        self.free_ranges.append(FreeRange(firstFreeDay, lastFreeDay, description))

    def add_free_ranges(self, free_ranges: list):
        self.free_ranges += free_ranges

    def is_working_day(self, day: datetime.date) -> bool:
        is_free_weekday = day.weekday() in self.free_weekdays
        is_holiday = any(free_range.contains(day) for free_range in self.free_ranges)
        return not(is_free_weekday or is_holiday)
