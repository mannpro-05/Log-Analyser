import sqlite3 as sl
from datetime import datetime
import inspect
from modules import app
import json
'''
input: ID of the record and the FILTERS section of the report
processing: Stores the record in the database with the id of the record to which it belongs.
Output: None
'''
def createFIlter(id, filters):
    conn = sl.connect('logs.db')
    now = datetime.now()
    app.logger.info(
        str(now.strftime("%H:%M %Y-%m-%d")) + ' ' + __file__ + ' ' + inspect.stack()[0][3] + ' ID: ' + str(id) + ' Value: ' + json.dumps(filters))
    for key,val in filters.items():
        if val == {}:
            continue
        conn.execute("INSERT INTO FILTERS VALUES (?,?,?,?)", (id, val["targetColumn"],val["condition"], val["value"]))
    conn.commit()
