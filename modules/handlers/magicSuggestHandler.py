import sqlite3 as sl
import json

def getData(column):
    conn = sl.connect('logs.db')
    cursor = conn.execute("SELECT * FROM %s"%(column))
    columnRecords = []
    for i in cursor.fetchall():
        columnRecords.append({
            "id" : i[0],
            "name" : i[1]
        })
    return json.dumps(columnRecords)