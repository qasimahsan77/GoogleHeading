"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
import urlparse
import requests
from bs4 import BeautifulSoup
import re
import time

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )

def GettingHotWords(Heading, HeadingLink, SearchKeyword):
    VowelLetters = ['and', 'is', 'in', 'on', 'if', 'the', 'they', 'that', 'which', 'how', 'out']
    HottestKeywords = []
    Total = 0
    while Total < len(Heading):
        url = urlparse.urlparse(HeadingLink[Total])
        SingleCharacter = ""
        #print('Removing Single Character')
        if not Heading[Total].__contains__('|'):
            SingleCharacter = re.sub(r"\b[a-zA-Z]\b", "", Heading[Total])
        else:
            SingleCharacter = re.sub(r"\b[a-zA-Z]\b", "", Heading[Total].split('|')[0])
        pass
        Letters = 0
        while Letters < len(VowelLetters):
            SingleCharacter = re.sub(r"\b" + str(VowelLetters[Letters]) + r"\b", "", SingleCharacter.lower())
            Letters += 1
        pass
        if " ".join(SingleCharacter.split()).replace('-', '').replace(url.netloc, '').__contains__(','):
            print(" ".join(SingleCharacter.split()).replace('-', '').replace(url.netloc, '').split(','))
            HottestKeywords.append(" ".join(SingleCharacter.split()).replace('-', '').replace('cnn.com', '').split(','))
        else:
            print(" ".join(SingleCharacter.split()).replace('-', '').replace(url.netloc, '').split(' '))
            HottestKeywords.append(" ".join(SingleCharacter.split()).replace('-', '').replace('cnn.com', '').split(' '))
        pass
        Total += 1
    pass
    return HottestKeywords
    pass

def GoogleHeadingScraper(SitesLink):
    Heading = []
    HeadingLink = []
    SearchKeyword = []
    Total = 0
    while Total < len(SitesLink):
        SearchURL=urlparse.urlparse(SitesLink[Total])
        Response = requests.get('https://www.google.com/search?q=site:' + SearchURL.netloc)
        if Response.status_code == 200:
            Soup = BeautifulSoup(Response.content, 'html.parser')
            Head = Soup.find('div', {'class': 'g'})
            if Head is not None:
                Title = Soup.find('h3')
                if Title is not None:
                    print('Title:{}'.format(Title.text.encode('ascii','ignore')))
                    Heading.append(Title.text.encode('ascii','ignore'))
                else:
                    Heading.append('N/A')
                pass
                Link = Soup.find('cite')
                if Link is not None:
                    print('Website:{}'.format(Link.text))
                    HeadingLink.append(Link.text)
                else:
                    HeadingLink.append('N/A')
                pass
                SearchKeyword.append(SitesLink[Total])
            pass
        else:
            print('Unable to Send Request on Google!')
        pass
        time.sleep(2)
        Total += 1
    pass
    HottestKeywords=GettingHotWords(Heading, HeadingLink, SearchKeyword)
    return Heading, HeadingLink, SearchKeyword,HottestKeywords
    pass

def google(request):
    """Renders the GoogleNews page."""
    Results = []
    Total = 0
    if request.method == 'POST':
        Links = request.POST.get('Keyword')
        SitesLink = Links.encode('ascii','ignore').split('\r\n')
        Total = len(SitesLink)
        Heading, HeadingLink, SearchKeyword,HottestKeywords = GoogleHeadingScraper(SitesLink)
        Results = zip(Heading, HeadingLink, SearchKeyword,HottestKeywords)
    return render(request, 'app/google.html', {
        'title':'Google Heading',
        'Results':Results,
        'Total':Total
    })