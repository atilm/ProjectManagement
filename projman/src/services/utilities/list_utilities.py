from typing import Iterable

def alignWidths(lhs : list, rhs : list, defaultEntry = 0) -> tuple:
    maxCount = max(len(lhs), len(rhs))
    lhs = fill_with(lhs, maxCount, defaultEntry)
    rhs = fill_with(rhs, maxCount, defaultEntry)
    return (lhs, rhs)

def fill_with(entries : list, count : int, defaultEntry) -> list:
    if len(entries) < count:
        result = entries + (count - len(entries)) * [defaultEntry]
    else:
        result = entries
    
    return result

def replace(objects: Iterable[object], candidate: object, matchComparison) -> bool:
    for i, o in enumerate(objects):
        if matchComparison(o, candidate):
            objects[i] = candidate
            return True
        
    return False