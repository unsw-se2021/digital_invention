# User System Class
from flask import request, render_template, url_for, redirect
from flask_login import UserMixin, login_manager, login_required, login_user, current_user, logout_user
import requests
from lxml import html
from User import User

BASE_URL = "https://webcms3.cse.unsw.edu.au"
LOGIN_URL = BASE_URL + "/login"
LOGOUT_URL = BASE_URL + "/logout"

class UserSystem():
    def __init__(self):
        self._users = {}

    def add_user(self, id, password):
        new_user = User(id, password)
        self._users[id] = new_user

    def authenticate_user(self, id, password):
        session = requests.session()
        result = session.get(LOGIN_URL)
        doc = html.fromstring(result.text)
        authenticity_token = list(set(doc.xpath("//input[@name='csrf_token']/@value")))[0] # change
        payload = {"zid": id, "password": password, "csrf_token": authenticity_token}
        result = session.post(LOGIN_URL, data = payload, headers = dict(referer = LOGIN_URL))
        for r in result.history:
            if LOGIN_URL == (r.url):
                if id not in self._users:
                    self.add_user(id, password)
                user = self._users[id]
                login_user(user)
                user.session = session
                return True
        return False

    def get_user(self, id):
        if id in self._users:
            return self._users[id]
        else:
            return None

    def log_out_user(self, id):
        self.navigateTo(id, LOGOUT_URL)
        logout_user(id)

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