from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
import re
import lxml
from urllib.error import HTTPError, URLError


subjectCode1 = 'COMP'
subjectCode2 = 'cs'
courseCode  = '3121'
year        = '19T1'
BASE_URL    = 'https://webcms3.cse.unsw.edu.au'
BASE_URL_2  = 'https://cgi.cse.unsw.edu.au'

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
        html = soup(response.read(), 'html.parser')
        print(html.geturl())
        element = html.find('meta', attrs={'http-equiv': 'refresh'})
        refreshContent = element['content']
        refUrl = refreshContent.partition('=')[2]
        response.close()
        return refUrl
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

courseCode = input("enter course code e.g. 1511: ")
#html = Urlopen('http://cgi.cse.unsw.edu.au/~' + subjectCode + courseCode + '/' + )
searchTerm = input("enter search term e.g. outline: ")
try:
    refUrl = followRefresh(BASE_URL + '/' + subjectCode1 + courseCode + '/' + year)
    html = Urlopen(refUrl)
    bs = soup(html.read(), 'lxml')
except:
    refUrl = followRefresh(BASE_URL_2 + '/' + '~' + subjectCode2 + courseCode + '/')
    html = Urlopen(refUrl)
    bs = soup(html.read(), 'lxml')

for ass in bs.find_all('a'):
    if searchTerm in str(ass).lower():
        print(genLink(refUrl, ass['href']))
