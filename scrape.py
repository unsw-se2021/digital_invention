import requests
from lxml import html
import re
import getpass
import tabula

LOGIN_URL = "https://webcms3.cse.unsw.edu.au/login"

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
    dashboard_url = "https://webcms3.cse.unsw.edu.au/dashboard"
    result = session_requests.get(dashboard_url, headers = dict(referer = dashboard_url))
    doc = html.fromstring(result.content)
    course = []
    print("Your courses:")
    nav = doc.xpath('.//ul[@class="nav navbar-nav"]')[0]
    for item in nav:
        course.append(item.text_content())
        print(item.text_content())
    print()

    while True:
        # get course outline
        outline_url = input("Enter course outline URL: ")
        result = session_requests.get(outline_url, headers = dict(referer = outline_url))
        doc = html.fromstring(result.content)
        try:
            # check if there's a frame in the course outline page
            doc_frame = doc.xpath('.//iframe')[0]
            outline_url = doc_frame.get("src")
            # redirect to the frame URL
            result = session_requests.get(outline_url, headers = dict(referer = outline_url))
            doc = html.fromstring(result.content)
        except IndexError:
            try:
                # check if there's a PDF in the page
                pdf_frame = doc.xpath('.//object[@type="application/pdf"]')[0]
                outline_url = "https://webcms3.cse.unsw.edu.au" + pdf_frame.get("data")
                # redirect to the PDF URL
                result = session_requests.get(outline_url, headers = dict(referer = outline_url))
                # download the PDF
                with open("outline.pdf", "wb") as f:
                    f.write(result.content)
                # use tabula to convert all tables into a CSV
                pdf_csv = tabula.convert_into("outline.pdf", "outline.csv", output_format = "csv", pages = "all" multiple_tables = True)
            except IndexError:
                pass
            pass
        print()

        # parse course outline html for assignment dates
        assignment = {}
        # paragraph = doc.xpath('.//p')
        bullet_point = doc.xpath('.//li')
        table_row = doc.xpath('.//tr')
        merged = bullet_point + table_row
        assignment_flag = False
        for line in merged:
            line_formatted = line.text_content().strip()
            # search for references to assignments
            # assignment_search = re.search("(?i)(?!.*(released|out))((Assignment|Project)\s?[0-9]*)", line_formatted)
            assignment_search = re.search("(?i)(?!.*(released|out))(Assignment [0-9]+)", line_formatted)
            if (assignment_search):
                assignment_flag = True
                # search for a reference to a week in the same line
                week_search_1 = re.search("(?i)Week ([0-9]+)", line_formatted)
                week_search_2 = re.search("(?i)^([0-9]+)(st|nd|th)*\s+", line_formatted)
                if (week_search_1):
                    assignment[assignment_search.group(2)] = week_search_1.group(1)
                elif (week_search_2):
                    assignment[assignment_search.group(2)] = week_search_2.group(1)

        print("Assignment dates:")
        if (not assignment):
            if (assignment_flag):
                print("Assignments found, but no due dates listed")
            else:
                print("No assignments found")
        else:
            for a in assignment:
                print(a + " - Week " + assignment[a])
        print()
        
        break

    # log out
    logout_url = "https://webcms3.cse.unsw.edu.au/logout"
    result = session_requests.get(logout_url, headers = dict(referer = logout_url))
    print("Logged out")

if __name__ == '__main__':
    main()