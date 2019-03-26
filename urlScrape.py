from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.error import HTTPError, URLError

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


subjectCode = 'cs'
courseCode  = '2111'
html = Urlopen('http://cgi.cse.unsw.edu.au/~' + subjectCode + courseCode + '/')

bs = BeautifulSoup(html.read(), 'html.parser')
for ass in bs.find_all('Assignment'):
    print(ass)
print(bs.h1)
