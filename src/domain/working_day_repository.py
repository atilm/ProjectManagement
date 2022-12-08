import datetime

class FreeRange:
    def __init__(self, firstFreeDay: datetime.date, lastFreeDay: datetime.date) -> None:
        self.firstFreeDay = firstFreeDay
        self.lastFreeDay = lastFreeDay

    def contains(self, day: datetime.date) -> bool:
        return self.firstFreeDay <= day and day <= self.lastFreeDay

class WorkingDayRepository:
    def __init__(self) -> None:
        self.free_weekdays = set()
        self.free_ranges = []

    # takes Weekdays as arguments
    def set_free_weekdays(self, *args) -> None:
        for weekday in args:
            self.free_weekdays.add(weekday)

    def add_free_range(self, firstFreeDay: datetime.date, lastFreeDay: datetime.date) -> None:
        self.free_ranges.append(FreeRange(firstFreeDay, lastFreeDay))

    def is_working_day(self, day: datetime.date) -> bool:
        is_free_weekday = day.weekday() in self.free_weekdays
        is_holiday = any(free_range.contains(day) for free_range in self.free_ranges)
        return not(is_free_weekday or is_holiday)
