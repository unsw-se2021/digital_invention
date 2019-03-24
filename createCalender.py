from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

from datetime import datetime, timedelta
from csv_ical import Convert
import csv

def googleCalender():
    return None

def getEventObject():
    return None

# Convert to Google Calender
def calCsv(string, split):
    with open('calender.csv', 'w') as csvFile:
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

def calIcal():
    convert = Convert()
    csv_file_location = 'calender.csv'
    ical_file_location = 'calender.ics'
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




def createCalender(string, outFile, split):

    calCsv(string, split)
    if outFile == 'ical':
        calIcal()

if __name__ == '__main__':
    test_string = 'Final exam1,05/03/13,10:00,12:00,Worth 20%,UNSW,Final exam2,05/03/13,9:00,12:00,Worth 20%,UNSW,Final exam3,05/03/13,10:00,12:00,Worth 20%,UNSW,'
    createCalender(test_string, 'ical', 6)
