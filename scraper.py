from bs4 import BeautifulSoup as BS
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options

import time
import requests
import urllib.request
import webbrowser


# job webpage
url = "https://www.bika.net/poslovi/inozemstvo/"

# job locations
places = ['austrija', 'inozemstvo', 'nizozemska',
          'sjedinjene-americke-drzave', 'slovenija',
          'svicarska', 'belgija', 'irska', 'njemacka',
          'slovacka', 'svedska', 'ujedinjeno-kraljevstvo',]

# archived urls
visited = []

class Scrapp:
    
    """Scrape jobs from site without job title filter."""


    def __init__(self, url, place, profession):

        self.url = url
        self.place = place
        self.profession = profession

        self.open_url()
  
        
    def open_url(self):

        if self.place:
            print(self.place,' searching...')
        if self.place:
            self.url = self.url + self.place
        connection = requests.get(self.url)
        
        if connection:
            
            self.pretty_content(connection)
            
        else:
            pass


    def pretty_content(self, content):

        plain = content.text
        bs = BS(plain, 'html.parser')
        self.bs = bs
        
        self.dissection(bs)


    def dissection(self, bsoup):

        section = bsoup.find('ol', 
        attrs={'id':'jobs'}).find_all('div', 
        attrs={'class':'item_desc'})
        if section:
            self.save_data(section)


    def save_data(self, data):

        file = open('poslovi.html', 'a')
        for i in data:
            if self.profession in str(i):
                file.write(str(i)+'<br><br>')

        if self.url not in visited:
            visited.append(self.url)
    
        self.check_for_pagination()
        
    

    def check_for_pagination(self):
        
        try:
            
            pagination = self.bs.find('div', attrs={'class':'paginacija'})
            for data in pagination.find_all('a', href=True):
                if data['href'] not in visited:
                    self.__init__(data['href'], None, self.profession)
                    
        except AttributeError:
            pass
        
        
        

      
                
        
file = open('poslovi.html', 'a')
file.truncate(0)
file.write('<style> h2 a{font-size:20px; color:#6495ED} .item_desc{margin-left:30%;} .ad_tool,.ad_toolbox{display:None;} .list_02{text-align:left;} . </style>')
file.write('<h1>Bika poslovi</h1><br><br>')
file.close()

def run(title):
    for i in places:
        job = Scrapp(url, i, title)
    
    

