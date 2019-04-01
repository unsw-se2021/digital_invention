from lxml import html
from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
import re
import lxml
from urllib.error import HTTPError, URLError
import requests

BASE_URL        = "https://webcms3.cse.unsw.edu.au"
LOGIN_URL       = BASE_URL + "/login"
DASHBOARD_URL   = BASE_URL + "/dashboard"
LOGOUT_URL      = BASE_URL + "/logout"
subjectCode1    = 'COMP'
subjectCode2    = 'cs'
courseCode      = '3121'
year            = '19T1'
BASE_URL_2      = 'https://cgi.cse.unsw.edu.au'
CALENDAR_URL    = "https://student.unsw.edu.au/calendar"

# UrlOpen with error handling
def Urlopen(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        print(e)
        return None
    except URLError as e:
        print('The server could not be found')
        return None
    else:
        #print('It worked')
        return html

# Follow Meta Refrest Tag
def followRefresh(url):
    try:
        response = Urlopen(url)
        html = soup(response.read(), 'lxml')
        #print(html.geturl())
        #print(html.meta)
        element = html.find_all('meta')
        for e in element:
            #if 'URL'|'url' in (e['content']):
            refUrl = (e['content'].partition('=')[2])
            if 'http' in refUrl:
                response.close()
                return refUrl
        #refreshContent = element['content']
        #refUrl = refreshContent.partition('=')[2]
        response.close()
        return url
    except:
        return url

def cleanString(str):
    newstr = ""
    for i in range(0, len(str)):
        if str[i] == "\n":
            pass
        elif str[i] == " ":
            pass
        else:
            newstr+=str[i]
    return newstr


# Generate forward link
def genLink(base, forward):
    forward = cleanString(forward)
    ba = re.split('/', base)
    fo = re.split('/', forward)
    if BASE_URL_2 in forward:
        return forward
    elif BASE_URL in forward:
        return forward
    elif 'http' in forward:
        return forward
    for f in fo:
        found = False
        for b in ba:
            if f == b:
                found = True
        if found == False:
            if f[0] != '/' and base[-1] == '/':
                base = base + (f)
            elif base[-1] == '/' and f[0] == '/':
                f = f[1:]
                base = base + f
            else:
                base = base + '/' + (f)
    return base

'''
def genlink()
'''
# Generate Current Term

# Generate Course URL
def generateCourseLink(courseCode):
    return BASE_URL_2 + '/' + '~' + subjectCode2 + courseCode + '/'

# Get Links for Search term
def searchLinks(searchTerm, searchLink):
    links = []
    refUrl = followRefresh(searchLink)
    #print(refUrl)
    #refUrl = followRefresh(BASE_URL + '/' + 'SENG' + courseCode + '/' + year)
    html = Urlopen(refUrl)
    bs = soup(html.read(), 'lxml')
    for link in bs.find_all('a'):
        if searchTerm in str(link).lower():
            #print(refUrl, link['href'])
            found = genLink(refUrl, link['href'])
            if BASE_URL_2 in refUrl and Urlopen(found) == None:
                found = genLink(BASE_URL, link['href'])
            print(found)
            for l in links:
                if found == l:
                    pass
                else:
                    links.append(found)
            newLinks = searchLinks(searchTerm, found)
            print(newLinks)

    return links

def navigateTo(url, session):
    if url[:1] == "/":
        url = BASE_URL + url

    result = session.get(url, headers = dict(referer = url))
    doc = html.fromstring(result.content)

    return doc



if __name__ == "__main__":
    courseCode = input("enter course code e.g. 1511: ")
    searchTerm = input("enter search term e.g. outline: ")
    courseLink = generateCourseLink(courseCode)

    #courseLink = 'https://cgi.cse.unsw.edu.au/~cs1511/COMP1511/19T1/resources/23728/'
    print(searchLinks(searchTerm, courseLink))
