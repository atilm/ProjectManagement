import datetime
from typing import Iterator

def dateRange(start_date: datetime, end_date: datetime) -> Iterator[datetime.datetime]:
    day_count = (end_date - start_date).days + 1
    for current_date in (start_date + datetime.timedelta(n) for n in range(day_count)):
        yield current_date