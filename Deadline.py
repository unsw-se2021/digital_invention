# Deadline Class
class Deadline(object):
    def __init__(self, description, deadline, worth, location):
        self.description    = description
        self.deadline       = deadline
        self.worth          = worth
        self.location       = location

''' FORMAT
        GMT_OFF = '+11:00'      # PDT/MST/GMT-7
        EVENT = {
            'summary': 'Deliverable 5',
            'location': 'Unse Elec Building',
            'description': 'Presentation: Project debut',
            'start': { 'dateTime': '2019-04-04T09:00:00'+GMT_OFF},
            'end': { 'dateTime': '2019-04-04T11:00:00'+GMT_OFF}
        }
'''
