import sqlite3 as sl
import inspect
from modules import app
from datetime import datetime


def deleteReport(title):
    now = datetime.now()
    app.logger.info(
        str(now.strftime("%H:%M %Y-%m-%d")) + ' ' + __file__ + ' ' + inspect.stack()[0][3], ' Title: '+title)
    conn = sl.connect('logs.db')
    cursor = conn.execute(" SELECT ID FROM RECORDS_LIST WHERE TITLE = ?", (title,))
    id = cursor.fetchone()[0]
    conn.execute("DELETE FROM RECORDS_LIST WHERE TITLE = ?", (title,))
    conn.execute("DELETE FROM EMAIL WHERE ID = ?", (id,))
    conn.execute("DELETE FROM FILTERS WHERE ID = ?", (id,))
    conn.commit()
    return {"message":"Record with title: " + title + " has been deleted successfully!"}