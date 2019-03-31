# Course Class

class Course():
    def __init__(self, name, url, selected):
        self.name = name
        self.url = url
        self.selected = selected
        self.assignment = {}
        self.exam = {}
