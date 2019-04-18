# Deadline Class
from datetime import datetime
class Deadline(object):
    def __init__(self, description, deadline, worth, location):
        self.summary        = description
        self.deadline       = deadline #this must be in isoformat
        self.description    = worth
        self.location       = location

    def toString(self):
        return self.summary+','+self.deadline.strftime('%d/%m/%Y')+','+self.description+','+self.location

'''
FORMAT
        GMT_OFF = '+11:00'      # PDT/MST/GMT-7
        EVENT = {
            'summary': 'Deliverable 5',
            'location': 'Unse Elec Building',
            'description': 'Worth 20%',
            'start': { 'dateTime': '2019-04-04T09:00:00'+GMT_OFF},
            'end': { 'dateTime': '2019-04-04T11:00:00'+GMT_OFF}
        }
'''
if __name__ == '__main__':
    d1 = Deadline('Final exam1', '2019-04-04T09:00:00','Worth 20%','UNSW')
    print(d1.toString())
