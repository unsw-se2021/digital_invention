import requests
from lxml import html
import re
import getpass
import tabula

BASE_URL = "https://webcms3.cse.unsw.edu.au"
LOGIN_URL = BASE_URL + "/login"

def navigate_to(session, url):
    if url[:1] == "/":
        url = BASE_URL + url

    result = session.get(url, headers = dict(referer = url))
    doc = html.fromstring(result.content)

    return doc

def main():
    session = requests.session()

    # extract authenticity token
    result = session.get(LOGIN_URL)
    doc = html.fromstring(result.text)
    authenticity_token = list(set(doc.xpath("//input[@name='csrf_token']/@value")))[0]

    # get and compile login details
    payload = {
        "zid": input("Enter zID: "),
        "password": getpass.getpass("Enter password: "),
        "csrf_token": authenticity_token
    }
    print()

    # perform login
    result = session.post(LOGIN_URL, data = payload, headers = dict(referer = LOGIN_URL))
    print(result)

    # get list of courses
    dashboard_url = BASE_URL + "/dashboard"
    # result = session.get(dashboard_url, headers = dict(referer = dashboard_url))
    # doc = html.fromstring(result.content)
    doc = navigate_to(session, dashboard_url)

    course = []
    print("Your courses:")
    nav = doc.xpath('.//ul[@class="nav navbar-nav"]')[0]
    for item in nav:
        course.append({"name": item.text_content(), "url": item[0].get("href")})
        print(item.text_content())
    print()

    # while True:
    for c in course:
        print("Due dates for " + c["name"] + ":")
        # get course outline
        # curr_outline_url = input("Enter course outline URL: ")
        # print()
        # curr_outline_url = course_url[c]
        curr_course_url = BASE_URL + c["url"]
        # result = session.get(curr_course_url, headers = dict(referer = curr_course_url))
        # doc = html.fromstring(result.content)
        doc = navigate_to(session, curr_course_url)

        curr_outline_url = doc.xpath('.//a[text()="Course Outline"]')[0].get("href")

        # result = session.get(curr_outline_url, headers = dict(referer = curr_outline_url))
        # doc = html.fromstring(result.content)
        doc = navigate_to(session, curr_outline_url)

        # check if there's a frame in the course outline page
        doc_frame = doc.xpath('.//iframe')
        # check if there's a PDF in the page
        pdf_frame = doc.xpath('.//object[@type="application/pdf"]')

        if (doc_frame):
            curr_outline_url = doc_frame[0].get("src")
            # redirect to the frame URL
            # result = session.get(curr_outline_url, headers = dict(referer = curr_outline_url))
            # doc = html.fromstring(result.content)
            doc = navigate_to(session, curr_outline_url)
        elif (pdf_frame):
            curr_outline_url = BASE_URL + pdf_frame[0].get("data")
            # redirect to the PDF URL
            result = session.get(curr_outline_url, headers = dict(referer = curr_outline_url))
            # download the PDF
            with open("outline.pdf", "wb") as f:
                f.write(result.content)
            # use tabula to convert all tables into a CSV
            tabula.convert_into("outline.pdf", "outline.csv", output_format = "csv", pages = "all", multiple_tables = True, java_options = "-Dsun.java2d.cmm=sun.java2d.cmm.kcms.KcmsServiceProvider")
            with open("outline.csv") as of:
                merged = of.readlines()

        if (not pdf_frame):
            # paragraph = doc.xpath('.//p')
            bullet_point = doc.xpath('.//li')
            table_row = doc.xpath('.//tr')
            merged = bullet_point + table_row

        # let's see if there are any assignments or exams
        # any_assignment = re.search("(?i)\\b(assignment)\\b", doc.text_content())
        # any_exam = re.search("(?i)\\b(exam)\\b", doc.text_content())

        # parse course outline html for assignment dates
        assignment = {}
        exam = {}
        # due = {}
        for line in merged:
            if (not pdf_frame):
                line_formatted = line.text_content().strip()
            else:
                line_formatted = line

            # search for references to assignments
            # if (any_assignment):
            assignment_search = re.search("(?i)(?!.*(released|out))(assignment [0-9]+)", line_formatted)
            if (assignment_search):
                # search for a reference to a week in the same line
                week_search_1 = re.search("(?i)Week ([0-9]+)", line_formatted)
                week_search_2 = re.search("(?i)^([0-9]+)(st|nd|th)*\\b", line_formatted)
                if (week_search_1):
                    assignment[assignment_search.group(2)] = week_search_1.group(1)
                elif (week_search_2):
                    assignment[assignment_search.group(2)] = week_search_2.group(1)

            # search for references to exams
            # if (any_exam):
            exam_search = re.search("(?i)([\w-]+ exam\\b)", line_formatted)
            if (exam_search):
                week_search_1 = re.search("(?i)Week ([0-9]+)", line_formatted)
                week_search_2 = re.search("(?i)^([0-9]+)(st|nd|th)*\\b", line_formatted)
                if (week_search_1):
                    exam[exam_search.group(1)] = week_search_1.group(1)
                elif (week_search_2):
                    exam[exam_search.group(1)] = week_search_2.group(1)

            # search for references to due dates
            # if (any_due):
            # due_search = re.search("(?i)([\w-]+ [0-9]+ due\\b)", line_formatted)
            # if (due_search):
            #     week_search_1 = re.search("(?i)Week ([0-9]+)", line_formatted)
            #     week_search_2 = re.search("(?i)^([0-9]+)(st|nd|th)*\\b", line_formatted)
            #     if (week_search_1):
            #         due[due_search.group(1)] = week_search_1.group(1)
            #     elif (week_search_2):
            #         due[due_search.group(1)] = week_search_2.group(1)

            # search everywhere to see if there's a final exam
            # final_exam_search_1 = re.search("(?i)Exam Period", doc.text_content())
            # final_exam_search_2 = re.search("(?i)Final Exam\\b", doc.text_content())
            # if (final_exam_search_1 or final_exam_search_2):
            #     exam["Final Exam"] = "Exam Period"

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

        # print("Due dates:")
        # if (not due):
        #     print("No due dates found")
        # else:
        #     for d in due:
        #         print(d + " - Week " + due[d])
        # print()

        # break

    # log out
    logout_url = BASE_URL + "/logout"
    # result = session.get(logout_url, headers = dict(referer = logout_url))
    navigate_to(session, logout_url)
    print("Logged out")

if __name__ == '__main__':
    main()
