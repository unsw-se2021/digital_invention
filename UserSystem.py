# User System Class
from User import *

BASE_URL        = "https://webcms3.cse.unsw.edu.au"
LOGIN_URL       = BASE_URL + "/login"
DASHBOARD_URL   = BASE_URL + "/dashboard"

class UserSystem(object):
    def __init__(self, user):
        self._user = user

    @property
    def user(self):
        return self._user
    @user.setter
    def user(self, user):
        self._user = user




    def navigateTo(self, url):
        if url[:1] == "/":
            url = BASE_URL + url

        result = self.user._session.get(url, headers = dict(referer = url))
        doc = html.fromstring(result.content)

        return doc

    # Populate Courses
    def populateCourses(self):
        doc = self.navigateTo(DASHBOARD_URL)

        courses = []
        #print("Your courses:")
        nav = doc.xpath('.//ul[@class="nav navbar-nav"]')[0]
        for item in nav:
            courses.append({"name": item.text_content(), "url": item[0].get("href")})
            #print(item.text_content())
        return courses

    # Log Out


if __name__ == "__main__":
    test_user = User('z5170340', 'Fake')
    print(test_user.authenticate())
    test_user_system = UserSystem(test_user)
    #test_user_system = UserSystem(test_user)
    #print(test_user_system.authenticate())
