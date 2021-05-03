import sqlite3 as sl
from modules.getData import getFinalData
from datetime import datetime
import inspect
from modules import app
import time
from modules.handlers import joinHandler
'''
input: Id of the report.
processing: Builds the sql query from the filters of the report and then the query is appended to the output from the 
joinHandler's sql query. After the complete query is built the data is retrived and returned.
Output: returns the final data.
'''

exception = ['STATUS','UPLOAD','DOWNLOAD', 'DATE_TIME']

def queryCreater(id):
    now = datetime.now()
    app.logger.info(
        str(now.strftime("%H:%M %Y-%m-%d")) + ' ' + __file__ + ' ' + inspect.stack()[0][3] + ' ' + str(id))
    conn = sl.connect('logs.db')
    cursor = conn.execute("SELECT * FROM RECORDS_LIST WHERE ID = ?",(id,))
    records = cursor.fetchone()
    cursor = conn.execute("SELECT * FROM FILTERS WHERE ID = ?", (records[0],))
    filters = cursor.fetchall()
    l = []
    sql = joinHandler.createInnerJoinQuery(records[3].split(','))
    start = time.time()
    for filter in filters:
        if filter[1] == 'between':
            values = filter[3].split(',')
            l.append('(F.'+filter[1]+' '+filter[2]+' '+ values[0] +' AND '+   values[1] +')')
        else:
            if filter[1] in exception:
                l.append('(F.' + filter[1] + ' ' + filter[2] + ' ' + filter[3] + ')')
            else:
                cursor = conn.execute('SELECT ID FROM %s WHERE %s = ?'% (filter[1], filter[1]), (filter[3],))
                value = cursor.fetchone()
                if value != None:
                    l.append('(F.'+filter[1]+' '+ filter[2] +' '+str(value[0])+')')
    if len(l)>1:
        l = ' AND '.join(l)
        sql += " WHERE " + l
    elif len(l) == 0:
        sql = sql
    else:
        sql += " WHERE " + l[0]
    end = time.time()
    print('Time to create the sql query:',end-start)
    start = time.time()
    print(sql)
    cursor = conn.execute(sql)
    value = cursor.fetchall()
    end = time.time()
    print('Time to fetch the values from the final table:', end-start)
    if value == []:
        print("Empty!!",value)
        return []
    else:
        finalData, columns = getFinalData.getAllData(value, records[3].split(','))
        return finalData
