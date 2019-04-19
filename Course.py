# Course Class

class Course():

    def __init__(self, name, url):
        self._name = name
        self._url = url
        self._selected = False
        self._due_dates = []
        self._has_labs = False
        self._color = ['red lighten-1','pink lighten-2','purple lighten-2','deep-purple lighten-2','indigo lighten-1','cyan','teal lighten-1','green lighten-1','light-green','orange','deep-orange lighten-1'][int(name[-4:]) % 11]

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, name):
        self._name = name

    @property
    def url(self):
        return self._url
    @url.setter
    def url(self, url):
        self._url = url

    @property
    def selected(self):
        return self._selected
    @selected.setter
    def selected(self, selected):
        self._selected = selected

    @property
    def has_labs(self):
        return self._has_labs
    @has_labs.setter
    def has_labs(self, has_labs):
        self._has_labs = has_labs

    @property
    def due_dates(self):
        return self._due_dates
    @due_dates.setter
    def due_dates(self, due_dates):
        self._due_dates = due_dates

    @property
    def color(self):
        return self._color

class DueDate():
    def __init__(self, name, week):
        self._name = name
        self._week = week

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, name):
        self._name = name

    @property
    def week(self):
        return self._week
    @week.setter
    def week(self, week):
        self._week = week
