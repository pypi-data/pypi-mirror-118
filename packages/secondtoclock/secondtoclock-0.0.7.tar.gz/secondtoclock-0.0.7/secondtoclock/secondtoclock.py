def secToClock(sec):
    # Functions
    def isOneDigit(num):
        if num // 10 == 0:
            return True
        else:
            return False

    # Definitonsxq
    minustes = sec // 60
    seconds = sec % (minustes * 60)

    if minustes > 60:
        hours = minustes // 60
        minustes = minustes % (hours * 60)
    else:
        hours = 0

    if isOneDigit(hours) and isOneDigit(minustes) and isOneDigit(seconds):
        return f'0{hours}:0{minustes}:0{seconds}'
    elif not isOneDigit(hours) and isOneDigit(minustes) and isOneDigit(seconds):
        return f'{hours}:0{minustes}:0{seconds}'
    elif isOneDigit(hours) and not isOneDigit(minustes) and isOneDigit(seconds):
        return f'0{hours}:{minustes}:0{seconds}'
    elif not isOneDigit(hours) and isOneDigit(minustes) and not isOneDigit(seconds):
        return f'0{hours}:0{minustes}:{seconds}'
    elif not isOneDigit(hours) and not isOneDigit(minustes) and isOneDigit(seconds):
        return f'{hours}:{minustes}:0{seconds}'
    elif not isOneDigit(hours) and isOneDigit(minustes) and not isOneDigit(seconds):
        return f'{hours}:0{minustes}:{seconds}'
    elif isOneDigit(hours) and not isOneDigit(minustes) and not isOneDigit(seconds):
        return f'0{hours}:{minustes}:{seconds}'
    elif not isOneDigit(hours) and not isOneDigit(minustes) and not isOneDigit(seconds):
        return f'{hours}:{minustes}:{seconds}'
