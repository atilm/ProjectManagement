def calc_average(items: list, selectorFunction) -> float:
    if len(items) <= 0:
        return None
    
    sum = 0.0
    for item in items:
        sum += selectorFunction(item)

    average = sum / len(items)
    return average