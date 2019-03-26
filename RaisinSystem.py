from User import User
from UserSystem import UserSystem
from Courses import Courses
from CourseSystem import CourseSystem


def main():

    test_user = User('z5170340', 'fakepass')
    print(test_user.authenticate())
    test_user_system = UserSystem(test_user)
    test_user.courses = test_user_system.populateCourses()
    for course in test_user.courses:
        print(course["name"])



















if __name__ == "__main__":
    main()
