# Subject System Class

class CourseSystem(object):
    def __init__(self):

        # Get Course Data

        def getCourseData(self, course):

            curr_course_url = BASE_URL + course.url
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
                week_search_1 = re.search("(?i)Week ([0-9]+)", line_formatted)
                week_search_2 = re.search("(?i)^([0-9]+)(st|nd|th)*\\b", line_formatted)
                assignment_search = re.search("(?i)(?!.*(released|out))(assignment [0-9]+)", line_formatted)
                if (assignment_search):
                    # search for a reference to a week in the same line

                    if (week_search_1):
                        assignment[assignment_search.group(2)] = week_search_1.group(1)
                    elif (week_search_2):
                        assignment[assignment_search.group(2)] = week_search_2.group(1)

                # search for references to exams
                # if (any_exam):
                exam_search = re.search("(?i)([\w-]+ exam\\b)", line_formatted)
                if (exam_search):
                    #week_search_1 = re.search("(?i)Week ([0-9]+)", line_formatted)
                    #week_search_2 = re.search("(?i)^([0-9]+)(st|nd|th)*\\b", line_formatted)
                    if (week_search_1):
                        exam[exam_search.group(1)] = week_search_1.group(1)
                    elif (week_search_2):
                        exam[exam_search.group(1)] = week_search_2.group(1)

            course.assignment = assignment
            course.exam = exam

        # Convert Course Data to CSV


        # Convert Course Data to ICS


        # Connect to Google Calender


        # Generate Email
