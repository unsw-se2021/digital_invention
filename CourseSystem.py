# Subject System Class
from RaisinSystem import *
from Course import Course

class CourseSystem(object):
    def __init__(self):
        self.course = []

    def addNewCourse(self, user, newCourse):
        for c in user.courses:
            if c.name == newCourse:
                return "Already Exists!"
        if len(newCourse) == 8:
            newCourseFaculty = newCourse[:4]
            newCourseCode = newCourse[4:]
            #print(newCourseCode, newCourseFaculty)
            if newCourseFaculty == ('COMP' or 'SENG') and True == newCourseCode.isdigit():
                user.courses = (Course(newCourse, generateCourseLink(newCourseCode), False))
                return "Added!"

        return "Incorrect Format!"

    # Populate Courses
    def populateCourses(self, user):
        if len(user.courses) != 0:
            return False
        doc = navigateTo(DASHBOARD_URL, user.session)

        c = []
        #print("Your courses:")
        nav = doc.xpath('.//ul[@class="nav navbar-nav"]')[0]
        for item in nav:
            #courses.append({"name": item.text_content(), "url": item[0].get("href"), "do": False})
            #course = Course(item.text_content(), item[0].get("href"), False)
            user.courses = (Course(item.text_content(), item[0].get("href"), False))
            #print(item.text_content())
        return True

    # Convert Course Data to CSV


    # Convert Course Data to ICS


    # Connect to Google Calender


    # Generate Email
