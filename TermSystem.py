from RaisinSystem import *



CALENDAR_URL = "https://student.unsw.edu.au/calendar"

class Term(object):
    def __init__(self, container):
        self.container = container
        self.name = self.container.h2.string
        self.startDate = None
        self.endDate = None

class TermSystem(object):
    def __init__(self, url):
        self.url = url
        self.terms = []
        self.now = datetime.datetime.now()
        self.year = str(self.now.year)

    def getTermUrl(self):
        term = self.getTerm()
        u=self.year[-2:]+'T'
        if (term.name[-1]).isdigit() == True:
            u += term.name[-1:]
        else:
            u += '0'
        return u

    def getTerm(self):
        self.getTerms()
        self.getDates()
        for t in self.terms:
            if self.betweenDates(t.startDate, t.endDate, self.now):
                return t
        return None

    def betweenDates(self, startDate, endDate, compareDate):
        if compareDate >= startDate and compareDate <= endDate:
            return True
        return False

    def stringTodate(self, str):
        #print(str)
        if (str.split(' ')[-1]).isdigit() != True:
            str+=' {}'.format(self.year)
        try:
            return datetime.datetime.strptime(str, '%d %b %Y')
        except:
            return datetime.datetime.strptime(str, '%d %B %Y')

    def getTerms(self):
        html = Urlopen(self.url)
        bs = soup(html.read(), 'lxml')
        ## Grabs all containers that have the Term tables
        for c in bs.find_all("div", {"class":"page-content-section default-expanded"}):
            self.terms.append(Term(c))
        html.close()

    def getDates(self):
        for t in self.terms:
            t.container=(t.container.find_all('strong'))
            for i in range(len(t.container)):
                if (t.container[i].string == self.year):
                    #print(t.container)
                    t.startDate, t.endDate = (t.container[-3+i].string.split(" - "))
                    t.startDate=self.stringTodate(t.startDate)
                    t.endDate=self.stringTodate(t.endDate)

if __name__ == "__main__":
    #t = TermSystem(CALENDAR_URL).getTerm()
    #print(t.name, t.startDate, t.endDate)
    print(TermSystem(CALENDAR_URL).getTermUrl())
