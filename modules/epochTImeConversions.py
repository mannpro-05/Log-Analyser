import time
import datetime
'''
input: Epoch format date
processing: convert Epoch format date to human readable time.
Output: human readable date and time.
'''
def epotchToDateTime(data):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data))


'''
input: human readable date and time.
processing: convert human readable time to Epoch format date.
Output: Epoch format date.
'''
def dateTimeToEpotch(data):
    date = data.split(':')
    day = date[0].split('-')
    return int(datetime.datetime(int(day[0]), int(day[1]), int(day[2]), int(date[1]), int(date[2]), int(date[3])).timestamp())