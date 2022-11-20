from src.domain.task import Task
import datetime

def isNumberOrNone(o):
    return type(o) == int or type(o) == float or o == None

def isDateOrNone(o):
    return type(o) == datetime.date or o == None