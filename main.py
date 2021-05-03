import sqlite3 as sl
import time
import datetime
start = time.time()
conn = sl.connect('logs.db')
mapper = {
    "DATE_TIME": 3,
    "STATUS": 5,
    "UPLOAD": 7,
    "DOWNLOAD": 8,
    "CLIENT_IP": 10,
    "USERNAME": 11,
    "METHOD": 12,
    "URL": 13,
    "HTTP_REFERER": 14,
    "USERAGENT": 15,
    "FILTER_NAME": 17,
    "FILTER_REASON": 18,
    "CACHECODE": 20,
    "USER_GROUPS": 29,
    "REQUEST_PROFILES": 30,
    "APPLICATION_SIGNATURES": 31,
    "CATEGORIES": 32,
    "UPLOAD_CONTENT": 34,
    "DOWNLOAD_CONTENT": 35
}

months = {
    "Jan": 1,
    "Feb": 2,
    "Mar": 3,
    "Apr": 4,
    "May": 5,
    "Jun": 6,
    "Jul": 7,
    "Aug": 8,
    "Sep": 9,
    "Oct": 10,
    "Nov": 11,
    "Dec": 12
}

def line_split(row):
    lst = row.split('\t')
    return lst

exception = ['STATUS', 'UPLOAD', 'DOWNLOAD']
counter = 0
with open('small.log','r') as logs:
    for i in logs:
        lst = line_split(i)
        finalData = []
        counter += 1
        if len(lst) == 1 or 'date_time' in lst[3].strip('"'):
            continue
        try:
            for key, val in mapper.items():
                if key in exception:
                    finalData.append(lst[val].strip('"'))
                    continue
                elif key == 'DATE_TIME':
                    date = lst[val].strip('"').split(':')
                    day = date[0].split('/')
                    day[1] = months[day[1]]
                    finalData.append(
                        datetime.datetime(int(day[2]), int(day[1]), int(day[0]), int(date[1]), int(date[2]),
                                          int(date[3])).timestamp())
                    continue
                elif key == 'URL':
                    if lst[val].strip('"') != '-':
                        lst[val] = lst[val].split('/')[2].split(':')[0].strip('"')
                elif key == 'USERNAME':
                    lst[val] = lst[val].split('@')[0].strip('"')

                cursor = conn.execute("SELECT ID FROM %s WHERE %s = ?" % (key, key), (lst[val].strip('"'),))
                value = cursor.fetchone()
                if value == None:
                    id = conn.execute("SELECT count(ID) FROM %s" % (key))
                    id = id.fetchone()[0] + 1
                    finalData.append(id)
                    conn.execute("INSERT INTO %s VALUES(?,?)" % (key), (id, lst[val].strip('"')))
                else:
                    finalData.append(value[0])
            final = tuple(finalData)
            conn.execute("INSERT INTO FINAL_LOG VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", final)
            if counter % 100000 == 0:
                print(counter / 100000)
                conn.commit()
        except Exception as e:
            print(e)
        
    conn.commit()



end = time.time()
#conn.execute("INSERT INTO INSERT_TIME VALUES (?,?)",('shorten_logs',end-start))
#conn.commit()
print(end - start)