from flask import request, render_template, url_for, redirect
from flask_login import UserMixin, login_manager, login_required, login_user, current_user, logout_user
import requests
from lxml import html
import os
from User import User

BASE_URL = "https://webcms3.cse.unsw.edu.au"
LOGIN_URL = BASE_URL + "/login"
LOGOUT_URL = BASE_URL + "/logout"

# User system - handles authentication and user functions
class UserSystem():
    def __init__(self):
        self._users = {}

    def add_user(self, id, dummy):
        new_user = User(id, dummy)
        self._users[id] = new_user

    def authenticate_user(self, id, password):
        session = requests.session()
        result = session.get(LOGIN_URL)
        doc = html.fromstring(result.text)
        authenticity_token = list(set(doc.xpath("//input[@name='csrf_token']/@value")))[0]
        payload = {"zid": id, "password": password, "csrf_token": authenticity_token}
        result = session.post(LOGIN_URL, data = payload, headers = dict(referer = LOGIN_URL))
        for r in result.history:
            if LOGIN_URL == (r.url):
                if id not in self._users:
                    self.add_user(id, False)
                user = self._users[id]
                login_user(user)
                user.session = session
                return True
        if id == "z1111111" or id == "z3333333":
            # our dummy users
            if id not in self._users:
                self.add_user(id, True)
            user = self._users[id]
            login_user(user)
            user.session = session
            return True
        return False

    def is_dummy(self, id):
        return self._users[id].dummy

    def get_user(self, id):
        if id in self._users:
            return self._users[id]
        else:
            return None

    def log_out_user(self, id):
        self.navigateTo(id, LOGOUT_URL)
        try:
            os.remove("calendars/" + id + ".csv")
        except OSError:
            pass
        try:
            os.remove("calendars/" + id + ".ics")
        except OSError:
            pass
        logout_user()

    def navigateTo(self, id, url):
        result = self.getResult(id, url)
        return html.fromstring(result.content)

    def getResult(self, id, url):
        if url[:1] == "/":
            url = BASE_URL + url

        return self._users[id].session.get(url, headers = dict(referer = url))

    def add_courses(self, id, courses):
        self._users[id].courses = courses

    def get_courses(self, id):
        return self._users[id].courses

    # add due date unsorted
    def add_due_date(self, id, course, due_date):
        for c in self._users[id].courses:
            if c.name == course:
                for a in range (len(c.due_dates)):
                    if c.due_dates[a].name == due_date.name:
                        c.due_dates[a] = due_date
                        return
                c.due_dates.append(due_date)
                break

    def is_due_date(self, id, course, task_name):
        for c in self._users[id].courses:
            if c.name == course:
                for d in c.due_dates:
                    if d.name == task_name:
                        return True
        return False

    def clear_due_dates(self, id):
        for c in self._users[id].courses:
            c.due_dates = []
            c.has_labs = False

    def has_labs(self, id, course):
        for c in self._users[id].courses:
            if c.name == course:
                c.has_labs = True

    def get_due_dates(self, id, course):
        for c in self._users[id].courses:
            if c.name == course:
                return c.due_dates
