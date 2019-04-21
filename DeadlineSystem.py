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
from ics import Calendar, Event
import csv

SYSTEM_EMAIL    = 'systemraisin@gmail.com'
SYSTEM_PASSWORD = 'digital.Invention2019'
SYSTEM_SERVER   = 'smtp.gmail.com'

# Deadline system - handles due date exporting
class DeadlineSystem():
    def __init__(self):
        self.deadlines = []

    def sendEmail(self, userID, recieverEmail):
        try:
            server = smtplib.SMTP_SSL(SYSTEM_SERVER, 465)
            server.login(SYSTEM_EMAIL, SYSTEM_PASSWORD)
            subject = 'Raisin: Your calendar files are available'
            body = 'Hi!\n\nAttached are .csv and .ics files, which can be imported into a calendar of your choice.\n\nThanks for using Raisin, and all the best for the term ahead.\n\nSincerely, Raisin Team'

            msg = MIMEMultipart()
            msg['From']="Raisin Team"
            msg['To']=recieverEmail
            msg['Subject']=subject
            msg.attach(MIMEText(body, 'plain'))

            # build file names
            files = ['.csv','.ics']
            i=0
            for f in files:
                files[i]='calendars/'+userID+f
                i+=1
            for f in files:
                attachment = open(f, 'rb')
                part = MIMEBase('application', 'octet-stream')
                part.set_payload((attachment).read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', "attachment; filename= "+"calendar."+f[-3:])

                msg.attach(part)
                attachment.close()

            msg = msg.as_string()
            server.sendmail(SYSTEM_EMAIL, recieverEmail, msg)
            server.close()
            return "Email sent successfully"
        except Exception as error:
            # return error
            return "Error occurred, please try again"

    def googleCalendar(self, deadlines):
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
            # return ('Authentication has failed: {0}'.format(e))
            return "Error occurred, please try again"
        GCAL = discovery.build('calendar', 'v3', http=credential.authorize(Http()))
        count=0
        for deadline in deadlines:
            eve = self.getEventObject(deadline)
            if eve != None:
                count+=1
                e = GCAL.events().insert(calendarId='primary', sendNotifications=True, body=eve).execute()
        return ('Added {} events to your Google Calendar!'.format(count))
    
    def getEventObject(self, deadline):
        EVENT = {
            'summary': deadline.summary,
            'location': deadline.location,
            'description': deadline.description,
            'start': { 'dateTime': deadline.deadline.isoformat(), 'timeZone': 'Australia/Sydney'},
            'end': { 'dateTime': (deadline.deadline + timedelta(days=1)).isoformat(),'timeZone': 'Australia/Sydney'}
        }
        return EVENT

    # csv creator
    def calCsv(self, zid, deadlines):
        with open('calendars/' + zid + '.csv', 'w') as csvFile:
            csvWriter = csv.writer(csvFile)

            csvHeader = 'Subject,Start Date,End Date,All Day Event,Description,Location\n'
            csvFile.write(csvHeader)

            for d in deadlines:
                csvFile.write(d.summary+','+d.deadline.strftime('%Y/%m/%d')+','+(d.deadline + timedelta(days=1)).strftime('%Y/%m/%d')+',Yes,'+d.description+','+d.location+'\n')
            csvFile.close()

    # ics (apple calendar) creator
    def calIcal(self, zid, deadlines):
        c = Calendar()
        for d in deadlines:
            e = Event()
            e.name = d.summary
            e.begin = d.deadline.strftime('%Y/%m/%d')
            e.location = d.location
            e.description = d.description
            c.events.add(e)
        with open('calendars/' + zid + '.ics', 'w') as f:
            f.writelines(c)

    # create csv and ics files
    def createCalendar(self, zid, deadlines):
        self.calCsv(zid, deadlines)
        self.calIcal(zid, deadlines)
