import requests
from lxml import html
import re
import datetime

CALENDAR_URL = "https://student.unsw.edu.au/calendar"

def get_dates(term_num):
    session = requests.session()
    result = session.get(CALENDAR_URL, headers = dict(referer = CALENDAR_URL))
    doc = html.fromstring(result.content)

    start_week_str = doc.xpath(".//tr[contains(text(), 'Teaching period T" + str(term_num) + "')]")[0].text_content()
    start_week_date = re.search("(?i)Teaching period T" + str(term_num) + " ([0-9]+ (jan|feb|mar|apr|may|june|july|aug|sep|oct|nov|dec))", start_week_str).group(1)
    exam_week_str = doc.xpath(".//tr[contains(text(), 'Exams T" + str(term_num) + "')]")[0].text_content()
    exam_week_date = re.search("(?i)Exams T" + str(term_num) + " ([0-9]+ (jan|feb|mar|apr|may|june|july|aug|sep|oct|nov|dec))", start_week_str).group(1)

    # todo: create a dictionary of all weeks and their start dates using datetime
    # e.g.
    # week = {}
    # some for loop
    #     week[1] = datetime.datetime(whatever the first date is)
    #     week[2] = datetime.datetime(add on a week)
    #     ...
    #     week["exams"] = whatever
    # then return this dict to whoever asked for it