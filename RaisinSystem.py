from UserSystem import UserSystem
from Course import Course

import requests
from lxml import html
import re
import tabula

BASE_URL = "https://webcms3.cse.unsw.edu.au"
DASHBOARD_URL = BASE_URL + "/dashboard"

class RaisinSystem():
    def __init__(self):
        self._user_system = UserSystem()

    def authenticate_user(self, id, password):
        return self._user_system.authenticate_user(id, password)

    def get_user(self, id):
        return self._user_system.get_user(id)

    def log_out_user(self, id):
        self._user_system.log_out_user(id)

    def add_courses(self, id, courses):
        self._user_system.add_courses(id, courses)

    def populate_courses(self, id):
        doc = self._user_system.navigateTo(id, DASHBOARD_URL)
        courses = []
        nav = doc.xpath('.//ul[@class="nav navbar-nav"]')[0]
        for item in nav:
            courses.append(Course(item.text_content(), BASE_URL + item[0].get("href"), False))
        self.add_courses(id, courses)

    def get_courses(self, id):
        return self._user_system.get_courses(id)

    def navigateTo(self, id, url):
        return self._user_system.navigateTo(id, url)

    def getResult(self, id, url):
        return self._user_system.getResult(id, url)

    def get_due_dates(self, id):
        for c in self.get_courses(id):
            if not c.selected:
                continue
            print("Due dates for " + c.name + ":")
            # get course outline
            curr_course_url = c.url
            doc = self.navigateTo(id, curr_course_url)

            curr_outline_url = doc.xpath('.//a[text()="Course Outline"]')[0].get("href")

            doc = self.navigateTo(id, curr_outline_url)

            # check if there's a frame in the course outline page
            doc_frame = doc.xpath('.//iframe')
            # check if there's a PDF in the page
            pdf_frame = doc.xpath('.//object[@type="application/pdf"]')

            if (doc_frame):
                curr_outline_url = doc_frame[0].get("src")
                # redirect to the frame URL
                doc = self.navigateTo(id, curr_outline_url)
            elif (pdf_frame):
                curr_outline_url = BASE_URL + pdf_frame[0].get("data")
                # redirect to the PDF URL
                result = self.getResult(id, curr_outline_url)
                # download the PDF
                with open(c.name + "_outline.pdf", "wb") as f:
                    f.write(result.content)
                # use tabula to convert all tables into a CSV
                tabula.convert_into(c.name + "_outline.pdf", c.name + "_outline.csv", output_format = "csv", pages = "all", multiple_tables = True, silent = True, java_options = "-Dsun.java2d.cmm=sun.java2d.cmm.kcms.KcmsServiceProvider")
                with open(c.name + "_outline.csv") as of:
                    merged = of.readlines()

            if (not pdf_frame):
                bullet_point = doc.xpath('.//li')
                table_row = doc.xpath('.//tr')
                merged = bullet_point + table_row

            # parse course outline html for assignment dates
            assignment = {}
            exam = {}

            for line in merged:
                if (not pdf_frame):
                    line_formatted = line.text_content().strip()
                else:
                    line_formatted = line

                week_search_1 = re.search("(?i)Week ([0-9]+)", line_formatted)
                week_search_2 = re.search("(?i)^([0-9]+)(st|nd|th)*\\b", line_formatted)
                
                # search for references to assignments
                assignment_search = re.search("(?i)(?!.*(released|out))(assignment [0-9]+)", line_formatted)
                if (assignment_search):
                    # search for a reference to a week in the same line
                    if (week_search_1):
                        assignment[assignment_search.group(2)] = week_search_1.group(1)
                    elif (week_search_2):
                        assignment[assignment_search.group(2)] = week_search_2.group(1)

                # search for references to exams
                exam_search = re.search("(?i)([\w-]+ exam\\b)", line_formatted)
                if (exam_search):
                    if (week_search_1):
                        exam[exam_search.group(1)] = week_search_1.group(1)
                    elif (week_search_2):
                        exam[exam_search.group(1)] = week_search_2.group(1)

            print("Assignment dates:")
            if (not assignment):
                print("No assignments found")
            else:
                for a in assignment:
                    print(a + " - Week " + assignment[a])

            print()

            print("Exam dates:")
            if (not exam):
                print("No exams found")
            else:
                for e in exam:
                    print(e + " - Week " + exam[e])
            print()