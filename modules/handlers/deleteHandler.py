import sqlite3 as sl
import inspect
from modules import app
from datetime import datetime


def deleteReport(title, userid):
    now = datetime.now()
    app.logger.info(
        str(now.strftime("%H:%M %Y-%m-%d")) + ' ' + __file__ + ' ' + inspect.stack()[0][3], ' Title: '+title)
    conn = sl.connect('logs.db')
    cursor = conn.execute("SELECT ID FROM RECORDS_LIST WHERE TITLE = ? AND USERID = ?", (title, userid))
    id = cursor.fetchone()
    if id == None:
        return {"message":"Record with title: " + title + " was created by someone else. You do not have permission to delete this record!."}
    conn.execute("DELETE FROM RECORDS_LIST WHERE TITLE = ?", (title,))
    conn.execute("DELETE FROM EMAIL WHERE ID = ?", (id[0],))
    conn.execute("DELETE FROM FILTERS WHERE ID = ?", (id[0],))
    conn.commit()
    return {"message":"Record with title: " + title + " has been deleted successfully!"}