from src.global_settings import GlobalSettings
import datetime

def to_date_str(date: datetime.date) -> str:
    dt = datetime.datetime.combine(date, datetime.datetime.min.time())
    return dt.strftime(GlobalSettings.date_format)

def parse_to_date(dateStr: str) -> datetime.date:
    return datetime.datetime.strptime(dateStr, GlobalSettings.date_format).date()