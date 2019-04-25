from flask_login import UserMixin

# User objects - contains information about user
class User(UserMixin):
    def __init__(self, id, dummy):
        self._id = id
        self._courses = []
        self._session = None
        self._dummy = dummy

    @property
    def id(self):
        return self._id
    @id.setter
    def id(self, id):
        self._id = id

    @property
    def courses(self):
        return self._courses
    @courses.setter
    def courses(self, courses):
        self._courses = courses

    @property
    def session(self):
        return self._session
    @session.setter
    def session(self, session):
        self._session = session

    @property
    def dummy(self):
        return self._dummy
