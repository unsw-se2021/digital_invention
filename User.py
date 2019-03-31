# User class
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, password):
        self._id = id
        self._password = password
        self._courses = []
        self._session = None

    @property
    def id(self):
        return self._id
    @id.setter
    def id(self, id):
        self._id = id

    @property
    def password(self):
        return self._password
    @password.setter
    def password(self, password):
        self._password = password

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