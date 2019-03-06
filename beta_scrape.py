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
    else:
        pass

    with open("test.txt", "w") as f:
        f.write(doc.text_content())

        

    # log out
    logout_url = BASE_URL + "/logout"
    result = session_requests.get(logout_url, headers = dict(referer = logout_url))
    print("Logged out")

if __name__ == '__main__':
    main()