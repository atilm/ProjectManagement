import datetime

class WorkingDayRepository:
    def __init__(self) -> None:
        self.free_weekdays = set()

    # takes Weekdays as arguments
    def set_free_weekdays(self, *args) -> None:
        for weekday in args:
            self.free_weekdays.add(weekday)

    def is_working_day(self, day: datetime.date) -> bool:
        return not(day.weekday() in self.free_weekdays)
