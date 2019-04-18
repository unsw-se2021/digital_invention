# Course Class

class Course():

    def __init__(self, name, url, selected):
        self._name = name
        self._url = url
        self._selected = selected
        self._due_dates = []
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
        self._weighting = 0

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

    @property
    def weighting(self):
        return self._weighting
    @weighting.setter
    def weighting(self, weighting):
        self._weighting = weighting
