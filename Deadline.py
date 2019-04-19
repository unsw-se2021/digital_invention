# Deadline Class
from datetime import datetime
class Deadline(object):
    def __init__(self, description, deadline, worth, location):
        self.summary        = description
        self.deadline       = deadline
        self.description    = worth
        self.location       = location
