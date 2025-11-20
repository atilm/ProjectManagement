from projman.src.global_settings import GlobalSettings
import datetime

def to_date_str(date: datetime.date) -> str:
    dt = datetime.datetime.combine(date, datetime.datetime.min.time())
    return dt.strftime(GlobalSettings.date_format)

def parse_to_date(dateStr: str) -> datetime.date:
    return datetime.datetime.strptime(dateStr, GlobalSettings.date_format).date()

def to_days_str(days: float) -> str:
    return f"{days:.1f}"

def remove_suffix(s, suffix: str) -> str:
    if suffix and s.endswith(suffix):
        return s[:-len(suffix)]
    return s