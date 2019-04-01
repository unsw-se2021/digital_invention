# Course Class

class Course(object):
    def __init__(self, name, url, do):
        self.name         = name
        self.url          = url
        self.do           = do
        self._events      = []

    @property
    def events(self):
        return self._events
    @events.setter
    def events(self, event):
        self._events.append(event)
