import re

class GlobalSettings:
    date_format = r"%d-%m-%Y"
    date_regex = re.compile(r"\d\d-\d\d-\d{4}")
    date_range_regex = re.compile(f"(?P<first>{date_regex.pattern}).+(?P<last>{date_regex.pattern})")
    velocity_count = 30 # the number of data points to calculate the average velocity from
    no_velocity_ignored_warning = "Story {0} has no estimate or workdays and was ignored."