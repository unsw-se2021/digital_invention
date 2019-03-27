# User class
import requests
from lxml import html

BASE_URL        = "https://webcms3.cse.unsw.edu.au"
LOGIN_URL       = BASE_URL + "/login"
DASHBOARD_URL   = BASE_URL + "/dashboard"

class User():
    def __init__(self, zID, zPass):
        self._zID       = zID
        self._zPass     = zPass
        self._courses   = []
        self._session   = None

    @property
    def zID(self):
        return self._zID
    @zID.setter
    def zID(self, zID):
        self._zID = zID

    @property
    def zPass(self):
        return self._zPass
    @zPass.setter
    def zPass(self, zPass):
        self._zPass = zPass

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



    # Authenticate User and save session
    def authenticate(self):
        session = requests.session()
        result = session.get(LOGIN_URL)
        doc = html.fromstring(result.text)
        authenticity_token = list(set(doc.xpath("//input[@name='csrf_token']/@value")))[0]
        payload = {"zid": self._zID, "password": self._zPass, "csrf_token": authenticity_token}
        result = session.post(LOGIN_URL, data = payload, headers = dict(referer = LOGIN_URL))
        #print(html.fromstring(result.text))
        check = False
        for r in result.history:
            if LOGIN_URL == (r.url):
                check = True
        self._session = session
        return check



def white_test():
    test_user = User('z5170340', 'FakePassword')
    print(test_user.authenticate())
    #print(test_user.zID, test_user.zPass)

if (__name__ == "__main__"):
    print("Running Test!")
    white_test()
