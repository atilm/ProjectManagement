import datetime

class FreeRange:
    def __init__(self, firstFreeDay: datetime.date, lastFreeDay: datetime.date, description: str) -> None:
        self.firstFreeDay = firstFreeDay
        self.lastFreeDay = lastFreeDay
        self.description = description

    def contains(self, day: datetime.date) -> bool:
        return self.firstFreeDay <= day and day <= self.lastFreeDay

    def __eq__(self, other: object) -> bool:
        if isinstance(other, FreeRange):
            return other.firstFreeDay == self.firstFreeDay and\
                other.lastFreeDay == self.lastFreeDay and\
                other.description == self.description
        else:
            return False