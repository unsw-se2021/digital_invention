# Event System Class
from RaisinSystem import *
from Event import Event

class EventSystem(object):
    def __init__(self):
        self.events = ['Labs', 'Tests', 'Assignments', 'Exam', 'Project Milestones', 'Presentations']

    # Populates Tests
    def populateEvents(self, user):
        for c in user.courses:
            if len(c.events) == 0:
                for e in self.events:
                    c.events = Event(e)
