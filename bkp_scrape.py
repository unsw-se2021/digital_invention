import requests
from lxml import html
import re
import getpass
import tabula

BASE_URL = "https://webcms3.cse.unsw.edu.au"
LOGIN_URL = BASE_URL + "/login"

def main():
    session_requests = requests.session()

    # extract authenticity token
    result = session_requests.get(LOGIN_URL)
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
    result = session_requests.post(LOGIN_URL, data = payload, headers = dict(referer = LOGIN_URL))

    # get list of courses
    dashboard_url = BASE_URL + "/dashboard"
    result = session_requests.get(dashboard_url, headers = dict(referer = dashboard_url))
    doc = html.fromstring(result.content)
    # course_url = {}
    print("Your courses:")
    nav = doc.xpath('.//ul[@class="nav navbar-nav"]')[0]
    for item in nav:
        # course_url[item.text_content()] = BASE_URL + item[0].get("href") + "/outline"
        print(item.text_content())
    print()

    while True:
    # for c in course_url:
        # get course outline
        outline_url = input("Enter course outline URL: ")
        print()
        # outline_url = course_url[c]
        result = session_requests.get(outline_url, headers = dict(referer = outline_url))
        doc = html.fromstring(result.content)

        # check if there's a frame in the course outline page
        doc_frame = doc.xpath('.//iframe')
        # check if there's a PDF in the page
        pdf_frame = doc.xpath('.//object[@type="application/pdf"]')
        if (doc_frame):
            outline_url = doc_frame[0].get("src")
            # redirect to the frame URL
            result = session_requests.get(outline_url, headers = dict(referer = outline_url))
            doc = html.fromstring(result.content)
        elif (pdf_frame):
            outline_url = BASE_URL + pdf_frame[0].get("data")
            # redirect to the PDF URL
            result = session_requests.get(outline_url, headers = dict(referer = outline_url))
            # download the PDF
            with open("outline.pdf", "wb") as f:
                f.write(result.content)
            # use tabula to convert all tables into a CSV
            pdf_csv = tabula.convert_into("outline.pdf", "outline.csv", output_format = "csv", pages = "all", multiple_tables = True)

        # let's see if there are any assignments or exams
        any_assignment = re.search("(?i)\\b(assignment)\\b", doc.text_content())
        any_exam = re.search("(?i)\\b(exam)\\b", doc.text_content())

        # parse course outline html for assignment dates
        assignment = {}
        exam = {}
        # paragraph = doc.xpath('.//p')
        bullet_point = doc.xpath('.//li')
        table_row = doc.xpath('.//tr')
        merged = bullet_point + table_row
        for line in merged:
            line_formatted = line.text_content().strip()

            # search for references to assignments
            # assignment_search = re.search("(?i)(?!.*(released|out))((Assignment|Project)\s?[0-9]*)", line_formatted)
            assignment_search = re.search("(?i)(?!.*(released|out))(Assignment [0-9]+)", line_formatted)
            if (assignment_search):
                # search for a reference to a week in the same line
                week_search_1 = re.search("(?i)Week ([0-9]+)", line_formatted)
                week_search_2 = re.search("(?i)^([0-9]+)(st|nd|th)*\\b", line_formatted)
                if (week_search_1):
                    assignment[assignment_search.group(2)] = week_search_1.group(1)
                elif (week_search_2):
                    assignment[assignment_search.group(2)] = week_search_2.group(1)

            # search for references to exams
            exam_search = re.search("(?i)([\w-]+ Exam\\b)", line_formatted)
            if (exam_search):
                week_search_1 = re.search("(?i)Week ([0-9]+)", line_formatted)
                week_search_2 = re.search("(?i)^([0-9]+)(st|nd|th)*\\b", line_formatted)
                if (week_search_1):
                    exam[exam_search.group(1)] = week_search_1.group(1)
                elif (week_search_2):
                    exam[exam_search.group(1)] = week_search_2.group(1)

            # search everywhere to see if there's a final exam
            final_exam_search_1 = re.search("(?i)Exam Period", doc.text_content())
            final_exam_search_2 = re.search("(?i)Final Exam\\b", doc.text_content())
            if (final_exam_search_1 or final_exam_search_2):
                exam["Final Exam"] = "Exam Period"

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
        
        break

    # log out
    logout_url = BASE_URL + "/logout"
    result = session_requests.get(logout_url, headers = dict(referer = logout_url))
    print("Logged out")

if __name__ == '__main__':
    main()