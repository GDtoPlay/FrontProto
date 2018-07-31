import datetime

def InFiveMin(start, end):
    delay = end - start
    print(delay)
    if delay.total_seconds() > 300:
        return False
    return True
