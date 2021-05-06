import os
import time
import insertRecords

os.chdir('/var/log/safesquid/extended/')

cronTime =int(time.time())

for i in os.listdir():
    mTime = os.path.getmtime(i)
    cTime = os.path.getctime(i)
    if (cronTime >= int(cTime) and (cronTime - 900) <= int(cTime)):
        print(i, cTime)
        insertRecords.insertModifiedRecordsRecords(i,cronTime)

    elif (cronTime>= int(mTime) and (cronTime - 900) <= int(mTime)):
        print(i, mTime)
        insertRecords.insertModifiedRecordsRecords(i,cronTime - 900)
