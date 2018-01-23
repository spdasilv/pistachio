timeString = '1910'

def hourTomin(timeString):
    date = list(timeString)
    hour = int(date[0] + date[1])
    mins = (date[2] + date[3])
    mins = int(mins)
    mins = mins/60
    totalmins = hour*60 + mins*60
    return totalmins
print(hourTomin(timeString))