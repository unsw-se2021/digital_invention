# User System Class
from User import *
from RaisinSystem import *

class UserSystem(object):
    def __init__(self):
        self._users = []

    @property
    def users(self):
        return self._users
    @users.setter
    def users(self, user):
        self._users.append(user)

    # Get User
    def getUser(self, id):
        for u in self._users:
            if id == u.zID:
                return u
        return None

    # Log Out
    def logout(self, id):
        navigateTo(LOGOUT_URL, self.getUser(id).session)
        return "Logged Out!"


if __name__ == "__main__":
    test_user = User('z5170340', 'fake')
    #print(test_user.authenticate(test_user.id, test_user.pass))
    test_user_system = UserSystem()
    if test_user.authenticate() == True:
        test_user_system.users = test_user
        print((test_user_system.getUser(test_user.zID)).zID)
        test_user_system.logout(test_user.zID)
    #test_user_system = UserSystem(test_user)
    #print(test_user_system.authenticate())
