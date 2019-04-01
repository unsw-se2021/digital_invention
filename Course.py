# Course Class

class Course():
    def __init__(self, name, url, selected):
        self.name = name
        self.url = url
        self.selected = selected
        self.assignments = []
        self.exams = []

class Assignment():
    def __init__(self, name, week):
        self.name = name
        self.week = week
        self.weighting = 0

class ProjectMilestone():
    def __init__(self, name, week):
        self.name = name
        self.week = week
        self.weighting = 0