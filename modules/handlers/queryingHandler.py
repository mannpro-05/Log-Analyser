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
magicException = ['HTTP_REFERER','URL']

def queryCreater(id):
    now = datetime.now()
    app.logger.info(
        str(now.strftime("%H:%M %Y-%m-%d")) + ' ' + __file__ + ' ' + inspect.stack()[0][3] + ' ' + str(id))
    conn = sl.connect('logs.db')
    cursor = conn.execute("SELECT * FROM RECORDS_LIST WHERE ID = ?",(id,))
    records = cursor.fetchone()
    cursor = conn.execute("SELECT * FROM FILTERS WHERE ID = ?", (records[0],))
    filters = cursor.fetchall()
    finalFiltersArray = []

    sql,extraClause = joinHandler.createInnerJoinQuery(records[3].split(','))
    start = time.time()
    for filter in filters:
        l = []
        if filter[2] == 'between':
            values = filter[3].split(',')
            finalFiltersArray.append('(F.'+filter[1]+' '+filter[2]+' '+ values[0] +' AND '+   values[1] +')')
        elif filter[2] == '!=':
            cursor = conn.execute('SELECT ID FROM %s WHERE %s like ? ESCAPE ?' % (filter[1], filter[1]),
                                  ('%' + filter[3] + '%', '/'))
            value = cursor.fetchall()
            if value == []:
                return []
            else:
                for i in value:
                    l.append('(F.' + filter[1] + ' ' + filter[2] + ' ' + str(i[0]) + ')')
                l = ' AND '.join(l)
                l = '(' + l + ')'
            finalFiltersArray.append(l)
        else:
            if filter[1] in exception:
                temp = []
                for i in filter[3].split(','):
                    temp.append('(F.' + filter[1] + ' ' + filter[2] + ' ' + i + ')')
                finalFiltersArray.append('(' + ' OR '.join(temp) + ')')
            else:
                if filter[1] in magicException:
                    multipleUrl = []
                    for j in filter[3].split(','):
                        l = []
                        cursor = conn.execute('SELECT ID FROM %s WHERE %s like ? ESCAPE ?'% (filter[1], filter[1]), ('%'+j+'%','/'))
                        value = cursor.fetchall()
                        if value != []:
                            if len(value) > 1000:
                                counter = 1
                                l=[]
                                temp = []
                                for i in value:
                                    l.append('(F.' + filter[1] + ' ' + filter[2] + ' ' + str(i[0]) + ')')
                                    counter += 1
                                    if counter > 500:
                                        temp.append('('+' OR '.join(l)+')')
                                        l=[]
                                        counter = 1
                                    l = ' OR '.join(temp)
                            else:
                                for i in value:
                                    l.append('(F.'+filter[1]+' '+ filter[2] +' '+str(i[0])+')')
                                l = ' OR '.join(l)
                                l = '(' + l + ')'
                                multipleUrl.append(l)
                        else:
                            return []
                    finalFiltersArray.append('(' + ' OR '.join(multipleUrl) + ')')
                else:
                    temp = []
                    for i in filter[3].split(','):
                        temp.append('(F.' + filter[1] + ' ' + filter[2] + ' ' + i + ')')
                    finalFiltersArray.append('(' + ' OR '.join(temp) + ')')
    if "DATE_TIME" not in records[3].split(','):
        fields = records[3].split(',')
        fields.append('NUMBER_OF_HITS')
        if len(finalFiltersArray)>1:
            finalFiltersArray = ' AND '.join(finalFiltersArray)
            sql += " WHERE " + finalFiltersArray + extraClause
        elif len(finalFiltersArray) == 0:
            sql = sql + extraClause
        else:
            sql += " WHERE " + finalFiltersArray[0] + extraClause
    else:
        fields = records[3].split(',')
        if len(finalFiltersArray)>1:
            finalFiltersArray = ' AND '.join(finalFiltersArray)
            sql += " WHERE " + finalFiltersArray + extraClause
        elif len(finalFiltersArray) == 0:
            sql = sql + extraClause
        else:
            sql += " WHERE " + finalFiltersArray[0] + extraClause
    end = time.time()
    print(sql)
    print('Time to create the sql query:',end-start)
    start = time.time()
    cursor = conn.execute(sql)
    value = cursor.fetchall()
    end = time.time()
    print('Time to fetch the values from the final table:', end-start)
    if value == []:
        print("Empty!!",value)
        return []
    else:
        print(fields)
        finalData, columns = getFinalData.getAllData(value, fields)
        return finalData
