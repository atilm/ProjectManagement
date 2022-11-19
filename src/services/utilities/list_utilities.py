def alignWidths(lhs : list, rhs : list, defaultEntry = 0) -> tuple:
    maxCount = max(len(lhs), len(rhs))
    lhs = fill_with(lhs, maxCount, defaultEntry)
    rhs = fill_with(rhs, maxCount, defaultEntry)
    return (lhs, rhs)

def fill_with(entries : list, maxCount : int, defaultEntry) -> list:
    if len(entries) < maxCount:
        result = entries + (maxCount - len(entries)) * [defaultEntry]
    else:
        result = entries
    
    return result