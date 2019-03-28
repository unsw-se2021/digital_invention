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
        print('It worked')
        return html

# Follow Meta Refrest Tag
def followRefresh(url):
    try:
        #print(url)
        response = Urlopen(url)
        html = soup(response.read(), 'html.parser')
        #print(response.read())
        print(html.geturl())
        element = html.find('meta', attrs={'http-equiv': 'refresh'})
        #print(element)
        refreshContent = element['content']
        refUrl = refreshContent.partition('=')[2]
        #print(url)
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
    #print('->', forward)
    ba = re.split('/', base)
    fo = re.split('/', forward)
    #print('->', fo)
    if BASE_URL_2 in forward:
        return forward
    elif BASE_URL in forward:
        return forward
    elif 'http' in forward:
        return forward
    #i = 0
    for f in fo:
        found = False
        for b in ba:
            if f == b:
                found = True
        if found == False:
            #print('->', base, f)
            if f[0] != '/' and base[-1] == '/':
                base = base + (f)

            #print('->', f)
            elif base[-1] == '/' and f[0] == '/':
                f = f[1:]
                #print('->', f)
                base = base + f
            else:
                base = base + '/' + (f)
        #i+=1

    return base


#html = Urlopen('http://cgi.cse.unsw.edu.au/~' + subjectCode + courseCode + '/' + )
#subjectCode1 = input("enter course code e.g. COMP1511: ")
searchTerm = input("enter search term e.g. outline: ")
try:
    refUrl = followRefresh(BASE_URL + '/' + subjectCode1 + courseCode + '/' + year)
    html = Urlopen(refUrl)
    bs = soup(html.read(), 'lxml')
except:
    refUrl = followRefresh(BASE_URL_2 + '/' + '~' + subjectCode2 + courseCode + '/')
#print(refUrl)
    html = Urlopen(refUrl)
#html = Urlopen('https://www.google.com')
    bs = soup(html.read(), 'lxml')
#print(bs.body)

for ass in bs.find_all('a'):
    #print(ass['href'].partition('/'))

    if searchTerm in str(ass).lower():
        #print(ass['href'])
        print(genLink(refUrl, ass['href']))
    #print(genLink(refUrl, ass['href']))
#print(bs.h1)
