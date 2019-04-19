# Deadline System Class
from __future__ import print_function
from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from Deadline import Deadline

from datetime import datetime, timedelta
from csv_ical import Convert
import csv

SYSTEM_EMAIL    = 'systemraisin@gmail.com'
SYSTEM_PASSWORD = 'digital.Invention2019'
SYSTEM_SERVER   = 'smtp.gmail.com'

class DeadlineSystem(object):
    def __init__(self):
        self.deadlines = []
        self.time_now  = datetime.now().isoformat().partition('.')[0]

    def sendEmail(self, userID, recieverEmail):
        try:
            server = smtplib.SMTP_SSL(SYSTEM_SERVER, 465)
            server.login(SYSTEM_EMAIL, SYSTEM_PASSWORD)
            subject = 'Deadline: Files'
            body = 'Hey there,\n\nThank you for using Raisin Planner!\n\nHave a nice semester. We hope to see you again next time!\n\n\n- Raisin Team'

            msg = MIMEMultipart()
            msg['From']="Raisin Team"
            msg['To']=recieverEmail
            msg['Subject']=subject
            msg.attach(MIMEText(body, 'plain'))

            # build file names
            files = [userID+'.csv', userID+'.ics']
            for f in files:
                attachment = open(f, 'rb')
                part = MIMEBase('application', 'octet-stream')
                part.set_payload((attachment).read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', "attachment; filename= "+"Calender."+f[-3:])

                msg.attach(part)
                attachment.close()

            msg = msg.as_string()
            server.sendmail(SYSTEM_EMAIL, recieverEmail, msg)
            server.close()
            return "Email Sent!"
        except Exception as error:
            return error




    def googleCalender(self, deadlines):
        SCOPES = 'https://www.googleapis.com/auth/calendar'
        store = file.Storage('storage.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('client_secrets.json', SCOPES)
            #print(flow.redirect_uri)
            creds = tools.run_flow(flow, store)

        GCAL = discovery.build('calendar', 'v3', http=creds.authorize(Http()))
        for deadline in deadlines:
            e = GCAL.events().insert(calendarId='primary', sendNotifications=True, body=self.getEventObject(deadline)).execute()
        os.remove('storage.json')

    def gflow(self):
        SCOPES = 'https://www.googleapis.com/auth/calendar'
        flow = client.flow_from_clientsecrets('client_secrets.json', SCOPES)
        flow.redirect_uri = client.OOB_CALLBACK_URN
        return flow
        #flow.step2input('Code')

    def gcal(self, code, deadlines):
        flow = self.gflow()
        try:
            credential = flow.step2_exchange(code, http=Http())
        except client.FlowExchangeError as e:
            return ('Authentication has failed: {0}'.format(e))
        GCAL = discovery.build('calendar', 'v3', http=credential.authorize(Http()))
        count=0
        for deadline in deadlines:
            eve = self.getEventObject(deadline)
            if eve != None:
                count+=1
                e = GCAL.events().insert(calendarId='primary', sendNotifications=True, body=eve).execute()
        return ('Added {} events to your Google Calender!'.format(count))
    def getEventObject(self, deadline):
        GMT_OFF = '+11:00'
        if (deadline.checkPassed(self.time_now)) == True: return None
        EVENT = {
            'summary': deadline.summary,
            'location': deadline.location,
            'description': deadline.description,
            'start': { 'dateTime': self.time_now, 'timeZone': 'Australia/Sydney'},
            'end': { 'dateTime': deadline.deadline,'timeZone': 'Australia/Sydney'}
        }
        return EVENT

    # Convert to csv
    def calCsv(self, zid, deadlines):
        with open(zid+'.csv', 'w') as csvFile:
            csvWriter = csv.writer(csvFile)

            csvHeader = 'Subject,Start date,Start time,End date,End time,Description,Location\n'
            csvFile.write(csvHeader)

            for deadline in deadlines:
                csvFile.write(deadline.toString()+'\n')
            csvFile.close()


    # Convert to iCal

    def calIcal(self, zid):
        convert = Convert()
        csv_file_location = zid+'.csv'
        ical_file_location = zid+'.ics'
        csv_configs = {
            'HEADER_COLUMNS_TO_SKIP': 1,
            'CSV_NAME': 0,
            'CSV_START_DATE': 1,
            'CSV_END_DATE': 3,
            'CSV_DESCRIPTION': 5,
            'CSV_LOCATION': 6,
        }

        convert.read_csv(csv_file_location, csv_configs)
        i = 0
        while i < len(convert.csv_data):
            row = convert.csv_data[i]
            start_date = row[csv_configs['CSV_START_DATE']] + '-' + row[2]
            end_date = row[csv_configs['CSV_END_DATE']] + '-' + row[4]
            try:
                row[csv_configs['CSV_START_DATE']] = datetime.strptime(
                    start_date, '%Y/%m/%d-%H:%M:%S'
                )
                row[csv_configs['CSV_END_DATE']] = datetime.strptime(
                    end_date, '%Y/%m/%d-%H:%M:%S'
                )
                i += 1
            except ValueError:
                convert.csv_data.pop(i)
        convert.make_ical(csv_configs)
        convert.save_ical(ical_file_location)

    def createCalender(self, zid, deadlines):
        self.calCsv(zid, deadlines)
        self.calIcal(zid)

if __name__ == '__main__':
    test_string = 'Final exam1,2019-04-14T09:00:00,Worth 20%,UNSW=Final exam2,2019-04-16T09:00:00,Worth 20%,UNSW=Final exam3,2019-04-17T09:00:00,Worth 20%,UNSW'
    tt = test_string.split('=')
    d = []
    for t in tt:
        t = (t.split(','))
        d.append(Deadline(t[0], t[1], t[2], t[3]))

    deadlineSystem = DeadlineSystem()
    deadlineSystem.createCalender('z5170340', d)


    flow = deadlineSystem.gflow()
    code = input(flow.step1_get_authorize_url()+'\nCODE:')
    print(deadlineSystem.gcal(flow, code, d))
