from UserSystem import UserSystem
from Course import Course, DueDate
from DeadlineSystem import DeadlineSystem
from Deadline import Deadline
from datetime import datetime, timedelta
import requests
from lxml import html
import re
import tabula
import csv
import os

BASE_URL = "https://webcms3.cse.unsw.edu.au"
DASHBOARD_URL = BASE_URL + "/dashboard"
CALENDAR_URL = "https://student.unsw.edu.au/calendar"

class RaisinSystem():
    def __init__(self):
        self._user_system = UserSystem()
        self._deadline_system = DeadlineSystem()

    def authenticate_user(self, id, password):
        return self._user_system.authenticate_user(id, password)

    def get_user(self, id):
        return self._user_system.get_user(id)

    def log_out_user(self, id):
        self._user_system.log_out_user(id)

    def add_courses(self, id, courses):
        self._user_system.add_courses(id, courses)

    def populate_courses(self, id):
        courses = []
        num_courses = 0
        if self._user_system.is_dummy(id):
            # populating dummy users with courses
            if id == "z1111111":
                courses.append(Course("COMP1511", BASE_URL + "/COMP1511/19T1/"))
                courses.append(Course("COMP2521", BASE_URL + "/COMP2521/19T1/"))
                courses.append(Course("COMP1911", BASE_URL + "/COMP1911/19T1/"))
                self.add_courses(id, courses)
                return 3
            elif id == "z3333333":
                courses.append(Course("COMP2121", BASE_URL + "/COMP2121/19T1/"))
                courses.append(Course("COMP3311", BASE_URL + "/COMP3311/19T1/"))
                self.add_courses(id, courses)
                return 2
        else:
            # scraping list of courses from webcms navbar
            doc = self.navigateTo(id, DASHBOARD_URL)
            nav = doc.xpath('.//ul[@class="nav navbar-nav"]')[0]
            for item in nav:
                num_courses += 1
                courses.append(Course(item.text_content(), BASE_URL + item[0].get("href")))
            self.add_courses(id, courses)
            return num_courses

    def get_courses(self, id):
        return self._user_system.get_courses(id)

    def navigateTo(self, id, url):
        return self._user_system.navigateTo(id, url)

    def getResult(self, id, url):
        return self._user_system.getResult(id, url)

    def add_due_date(self, id, course, due_date):
        self._user_system.add_due_date(id, course, due_date)

    def clear_due_dates(self, id):
        self._user_system.clear_due_dates(id)

    def has_labs(self, id, course):
        self._user_system.has_labs(id, course)

    def get_due_dates(self, id, course):
        return self._user_system.get_due_dates(id, course)

    def is_due_date(self, id, course, task_name):
        return self._user_system.is_due_date(id, course, task_name)

    def gcal(self, code, deadlines):
        return self._deadline_system.gcal(code, deadlines)

    def sendEmail(self, userID, recieverEmail):
        return self._deadline_system.sendEmail(userID, recieverEmail)

    def createCalendar(self, zid, deadlines):
        self._deadline_system.createCalendar(zid, deadlines)

    def get_deadlines(self, id):
        courses = self.get_courses(id)
        deadlines = []
        # make this slightly less hard coded
        term_start = datetime.strptime("13/2/2019", "%d/%m/%Y")
        exam_start = datetime.strptime("2/5/2019", "%d/%m/%Y")
        for c in courses:
            for d in c.due_dates:
                if d.week == "Exam period":
                    due_date = exam_start
                    deadlines.append(Deadline(c.name + " - " + d.name, due_date, "During exam period", "UNSW"))
                else:
                    due_date = term_start + timedelta(days=7*(int(d.week) - 1))
                    deadlines.append(Deadline(c.name + " - " + d.name, due_date, "Due this week", "UNSW"))
        return deadlines

    # def get_dates(self):
    #     # separate session from webcms
    #     session = requests.session()
    #     result = session.get(CALENDAR_URL, headers = dict(referer = CALENDAR_URL))
    #     doc = html.fromstring(result.content)

    #     for t in range(1,4):
    #         print(str(t))
    #         start_week = False
    #         exam_week = False
    #         all_tables = doc.xpath(".//tr")
    #         for table in all_tables:
    #             table = table.text_content()
    #             print(table)
    #             if not start_week:
    #                 start_week = re.search("(?i)Teaching period T" + str(t) + "([0-9]+ (jan|feb|mar|apr|may|june|july|aug|sep|oct|nov|dec))", table)
    #             if not exam_week:
    #                 exam_week = re.search("(?i)Exams T" + str(t) + "([0-9]+ (jan|feb|mar|apr|may|june|july|aug|sep|oct|nov|dec))", table)
    #             if start_week and exam_week:
    #                 break

    #         start_week_date = datetime.strptime(start_week.group(1) + " 2019", "%d %b %Y")
    #         exam_week_date = datetime.strptime(start_week.group(1) + " 2019", "%d %b %Y")

    #         if datetime.now() < exam_week_date:
    #             return (start_week_date, exam_week_date) 

    # parse all selected due dates from course outlines
    def scrape_due_dates(self, id, find_assignments, find_exams, find_milestones, find_labs):
        self.clear_due_dates(id)
        for c in self.get_courses(id):
            if not c.selected:
                continue
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
                with open("tempfiles/" + id + "_" + c.name + "_outline.pdf", "wb") as f:
                    f.write(result.content)
                # use tabula to convert all tables into a CSV
                tabula.convert_into("tempfiles/" + id + "_" + c.name + "_outline.pdf", "tempfiles/" + id + "_" + c.name + "_outline.csv", output_format = "csv", pages = "all", lattice = True, multiple_tables = True, silent = True, java_options = "-Dsun.java2d.cmm=sun.java2d.cmm.kcms.KcmsServiceProvider")
                merged = []
                whole_doc = ""
                with open("tempfiles/" + id + "_" + c.name + "_outline.csv") as of:
                    of_reader = csv.reader(of, delimiter = ",")
                    for row in of_reader:
                        merged.append(" ".join(row))
                        whole_doc += " " + " ".join(row)
                os.remove("tempfiles/" + id + "_" + c.name + "_outline.pdf")
                os.remove("tempfiles/" + id + "_" + c.name + "_outline.csv")

            if (not pdf_frame):
                bullet_point = doc.xpath('.//li')
                table_row = doc.xpath('.//tr')
                # paragraph = doc.xpath('.//p')
                # code = doc.xpath('.//pre')
                # merged = bullet_point + table_row + paragraph + code
                merged = bullet_point + table_row
                whole_doc = doc.text_content()

            # our list of searches, which we'll be adding to
            # change depending on criteria selected
            searches = []
            if find_assignments:
                searches.append("((?i)(?!.*(released|out))(assignment [0-9]+))")
            if find_exams:
                searches.append("((?i)([\w-]+ exam\\b))")

            # search everywhere to see if there's X due
            # only if project milestones is selected
            if find_milestones:
                x_due_search = re.findall("(?i)(([\w-]+) [0-9]+ due\\b)", whole_doc)
                for x in x_due_search:
                    if not x[1].lower() == "assignment" and "((?i)(?!.*(released|out))(" + x[1].lower() + " [0-9]+))" not in searches:
                        # print("adding " + x[1])
                        searches.append("((?i)(?!.*(released|out))(" + x[1].lower() + " [0-9]+))")

            for line in merged:
                if (not pdf_frame):
                    line_formatted = line.text_content().strip()
                else:
                    line_formatted = line

                week_search = []
                week_search.append(re.search("(?i)week ([0-9]+)", line_formatted))
                week_search.append(re.search("(?i)^([0-9]+)(st|nd|th)*\\b", line_formatted))

                for s in searches:
                    # search for references to above terms
                    date_search = re.findall(s, line_formatted)
                    for d in date_search:
                        # search for a reference to a week in the same line
                        for w in week_search:
                            if (w):
                                if (int(w.group(1)) < 12):
                                    self.add_due_date(id, c.name, DueDate(d[0].capitalize(), w.group(1)))
                                    break
                        # add to the estimator(tm)

            # search everywhere to see if there are labs
            # only if labs selected
            if find_labs:
                lab_search_1 = re.search("(?i)\\blab\\b", whole_doc)
                lab_search_2 = re.search("(?i)laborator(y|ies)", whole_doc)
                if (lab_search_1 or lab_search_2):
                    self.has_labs(id, c.name)

            # search everywhere to see if there's a final exam
            # only if exams selected
            if find_exams:
                final_exam_search_1 = re.search("(?i)exam period", whole_doc)
                final_exam_search_2 = re.search("(?i)final exam\\b", whole_doc)
                if (final_exam_search_1 or final_exam_search_2):
                    self.add_due_date(id, c.name, DueDate("Final exam", "Exam period"))

            # see if there are assignments with no due dates (a la 2521, thanks for nothing)
            # then estimate the due dates (not the greatest implementation)
            if find_assignments:
                test_highest = 0
                test_assignment_search = re.findall("((?i)(assignment ([0-9]+)))", whole_doc)
                for t in test_assignment_search:
                    if not self.is_due_date(id, c.name, t[0].capitalize()):
                        test_highest = int(t[2])
                if test_highest == 2:
                    self.add_due_date(id, c.name, DueDate("Assignment 1 (estimated)", "4"))
                    self.add_due_date(id, c.name, DueDate("Assignment 2 (estimated)", "9"))
                elif test_highest == 3:
                    self.add_due_date(id, c.name, DueDate("Assignment 1 (estimated)", "3"))
                    self.add_due_date(id, c.name, DueDate("Assignment 2 (estimated)", "6"))
                    self.add_due_date(id, c.name, DueDate("Assignment 3 (estimated)", "9"))
