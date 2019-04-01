from UserSystem import UserSystem
from Course import Course, DueDate
import requests
from lxml import html
import re
import tabula
import csv
import os

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
        doc = self.navigateTo(id, DASHBOARD_URL)
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

    def add_due_date(self, id, course, due_date):
        self._user_system.add_due_date(id, course, due_date)

    def get_due_dates(self, id, course):
        return self._user_system.get_due_dates(id, course)

    # rory's big parser
    def scrape_due_dates(self, id):
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
                with open("tempfiles/" + c.name + "_outline.pdf", "wb") as f:
                    f.write(result.content)
                # use tabula to convert all tables into a CSV
                tabula.convert_into("tempfiles/" + c.name + "_outline.pdf", "tempfiles/" + c.name + "_outline.csv", output_format = "csv", pages = "all", lattice = True, multiple_tables = True, silent = True, java_options = "-Dsun.java2d.cmm=sun.java2d.cmm.kcms.KcmsServiceProvider")
                merged = []
                with open("tempfiles/" + c.name + "_outline.csv") as of:
                    of_reader = csv.reader(of, delimiter = ",")
                    for row in of_reader:
                        merged.append(" ".join(row))
                os.remove("tempfiles/" + c.name + "_outline.pdf")
                os.remove("tempfiles/" + c.name + "_outline.csv")

            if (not pdf_frame):
                # bullet_point = doc.xpath('.//li')
                table_row = doc.xpath('.//tr')
                # merged = bullet_point + table_row
                merged = table_row

            # parse course outline html for assignment dates
            # assignment = {}

            for line in merged:
                if (not pdf_frame):
                    line_formatted = line.text_content().strip()
                else:
                    line_formatted = line

                searches = ["((?i)(?!.*(released|out))(assignment [0-9]+))", "((?i)((del|deliverable) [0-9]+))", "((?i)([\w-]+ exam\\b))"]

                week_search_1 = re.search("(?i)Week ([0-9]+)", line_formatted)
                week_search_2 = re.search("(?i)^([0-9]+)(st|nd|th)*\\b", line_formatted)
                
                for s in searches:
                    # search for references to assignments
                    date_search = re.findall(s, line_formatted)
                    for d in date_search:
                        # search for a reference to a week in the same line
                        if (week_search_1):
                            self.add_due_date(id, c.name, DueDate(d[0], "Week " + week_search_1.group(1)))
                            # assignment[d[0]] = week_search_1.group(1)
                        elif (week_search_2):
                            self.add_due_date(id, c.name, DueDate(d[0], "Week " + week_search_2.group(1)))
                            # assignment[d[0]] = week_search_2.group(1)

            # search everywhere to see if there's a final exam
            final_exam_search_1 = re.search("(?i)Exam Period", doc.text_content())
            final_exam_search_2 = re.search("(?i)Final Exam\\b", doc.text_content())
            if (final_exam_search_1 or final_exam_search_2):
                self.add_due_date(id, c.name, DueDate("Final Exam", "Exam Period"))

            # print("Due dates:")
            # if (not assignment):
            #     print("No dates found")
            # else:
            #     for a in assignment:
            #         print(a + " - Week " + assignment[a])