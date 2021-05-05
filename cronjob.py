from datetime import datetime
import sqlite3 as sl
from modules import app
from modules.mailDict import sendMail
from modules.handlers import handleDownloads
conn = sl.connect('logs.db')

cursor = conn.execute("SELECT * FROM EMAIL")
value = cursor.fetchall()
minute = ''
now = datetime.now()
print(now.strftime("%H:%M %Y-%m-%d"))
if now.minute < 10:
    minute = '0'+str(now.minute)
else:
    minute = str(now.minute)

for emails in value:
    print(emails, now)
    if emails[2] == 'Daily':
        if(((str(now.hour)+':'+str(int(minute) - 5)) >= emails[3]) and (emails[3] <= (str(now.hour)+':'+str(int(minute) - 5)))):
            with app.app_context():
                fileName = handleDownloads.createDownloadFile(id = emails[0],fileType = 'csv', pythonFileName = "cronjob")
                sendMail.sendMail(emails[1],fileName)
    elif emails[2] == 'Weekly':
        if ((((str(now.hour)+':'+str(int(minute) - 5)) >= emails[3].split(',')[0]) and (emails[3].split(',')[0] <= (str(now.hour)+':'+str(int(minute) - 5))))\
                and (datetime.today().strftime('%A') == emails[3].split(',')[1])):
            fileName = handleDownloads.createDownloadFile(id = emails[0],fileType = 'csv', pythonFileName = "cronjob")
            with app.app_context():
                sendMail.sendMail(emails[1], fileName)
    else:
        if (((((str(now.hour)+':'+str(int(minute) - 5)) >= emails[3].split(',')[0]) and (emails[3].split(',')[0] <= (str(now.hour)+':'+str(int(minute) - 5)))))\
                and (emails[3].split(',')[1] == str(now.day))):
            fileName = handleDownloads.createDownloadFile(id = emails[0],fileType = 'csv', pythonFileName = "cronjob")
            with app.app_context():
                sendMail.sendMail(emails[1], fileName)

                '''with app.app_context():
    sendMail.sendMail("mannprajapati567@gmail.com")'''
