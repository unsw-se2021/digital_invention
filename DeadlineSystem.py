# Deadline System Class

from __future__ import print_function
from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
import os

from datetime import datetime, timedelta
from csv_ical import Convert
import csv

class DeadlineSystem(object):
    def __init__(self):
        self.deadlines = []

    def googleCalender(self):
        SCOPES = 'https://www.googleapis.com/auth/calendar'
        store = file.Storage('storage.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('client_secrets.json', SCOPES)
            creds = tools.run_flow(flow, store)
        GCAL = discovery.build('calendar', 'v3', http=creds.authorize(Http()))
        for deadline in deadlines:
            e = GCAL.events().insert(calendarId='primary', sendNotifications=True, body=getEventObject(deadline)).execute()
        os.remove('storage.json')

    def getEventObject(self, deadline):
        GMT_OFF = '+11:00'
        EVENT = {
            'summary': deadline.description,
            'location': deadline.location,
            'description': deadline.worth,
            'start': { 'dateTime': datetime.datetime.now().isoformat()},
            'end': { 'dateTime': deadline.deadline}
        }
        return EVENT

    # Convert to csv
    def calCsv(self, zid, string, split):
        with open(zid+'.csv', 'w') as csvFile:
            csvWriter = csv.writer(csvFile)
            i = 0
            line = ''
            if split == 6:
                csvHeader = 'Subject,Start date,Start time, End date, Description, Location\n'
            csvFile.write(csvHeader)
            for token in string.split(','):

                if i == 0:
                    line = line + token
                elif i < split:
                    line = line + ',' + token
                else:
                    #print(line)
                    line = line + '\n'
                    csvFile.write(line)
                    i = 0
                    line = '' + token

                i = i + 1

            csvFile.write(line)
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
            'CSV_DESCRIPTION': 4,
            'CSV_LOCATION': 5,
        }

        convert.read_csv(csv_file_location, csv_configs)
        i = 0
        while i < len(convert.csv_data):
            row = convert.csv_data[i]
            start_date = row[csv_configs['CSV_START_DATE']] + '-' + row[2]
            try:
                row[csv_configs['CSV_START_DATE']] = datetime.strptime(
                    start_date, '%m/%d/%y-%H:%M'
                )
                row[csv_configs['CSV_END_DATE']] = \
                    row[csv_configs['CSV_START_DATE']]+timedelta(hours=1)
                i += 1
            except ValueError:
                convert.csv_data.pop(i)

        convert.make_ical(csv_configs)
        convert.save_ical(ical_file_location)

    def createCalender(self, zid, string, outFile, split):

        self.calCsv(zid, string, split)
        if outFile == 'ical':
            self.calIcal(zid)

if __name__ == '__main__':
    test_string = 'Final exam1,05/03/13,10:00,12:00,Worth 20%,UNSW,Final exam2,05/03/13,9:00,12:00,Worth 20%,UNSW,Final exam3,05/03/13,10:00,12:00,Worth 20%,UNSW,'
    deadlineSystem = DeadlineSystem()
    deadlineSystem.createCalender('z5170340', test_string, 'ical', 6)
    deadlineSystem.googleCalender()
