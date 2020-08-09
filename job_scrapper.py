import time
import requests
import urllib.request
import webbrowser
from bs4 import BeautifulSoup as BS



class FileManager:

    """ Stores data int file created in initiate_file() method.
        Creates file at beggining of script from Control class.
    """
    
    def save_data(self, data):

        file = open('poslovi.html', 'a')
        for i in data:
            file.write(i)
        file.close()

            

    def initiate_file(self, error_msg=False):
    
        file = open('poslovi.html', 'a')
        file.truncate(0)
        file.write('<style> h2 a{font-size:20px; color:#6495ED} .item_desc{margin-left:30%;}\
                   .ad_tool,.ad_toolbox{display:None;} .list_02{text-align:left;} . </style>\
                   <h1>Bika poslovi</h1><br><br>')
        if error_msg:
            file.write("<h1>Sommething went wrong in Control class.</h1><br>\
                        <p>Check for title and places data.</p>")
        file.close()
        




class WebScrapper:
    
    """Scrape jobs from site without job title filter.
       Traverses thru pagination.
    """


    def __init__(self, url, job, place):

        self.url = url
        self.job = job
        self.place = place
        self.open_url(self.url_control())


    def add_to_visited_sites(self, url):
        self.visited.append(url)        


    def url_control(self, url=None):
        
        if url == None:
            url = self.url + self.place
        if url in self.visited:
            return None
        self.add_to_visited_sites(url)
        return url
        

        
    def open_url(self, url):
        if url == None:
            return
        connection = requests.get(url)
        if connection:
            self.pretty_content(connection)
        pass


    def pretty_content(self, content):

        plain = content.text
        bs = BS(plain, 'html.parser')
        self.bs = bs
        self.list_jobs(bs)


    def list_jobs(self, bsoup):

        section = bsoup.find('ol', 
        attrs={'id':'jobs'}).find_all('div', attrs={'class':'item_desc'})       # Get page section with job items, scrap and compare it with target job
        if section: 
            for i in section:
                for job in self.jobs:
                    if job in str(i):
                        self.data.append(str(i) + "<br><br>")                       # Store persistant valid data to list located in Control class
            self.check_for_pagination()


    def check_for_pagination(self):
                                        # Avoid Selenium by checking element existance
        try:
            pagination = self.bs.find('div', attrs={'class':'paginacija'})
            for data in pagination.find_all('a', href=True):
                self.open_url(self.url_control(data['href']))         
        except AttributeError:
            pass




class IODataHandler(WebScrapper):



    def __init__(self, url,jobs, places):

        self.url = url
        self.jobs = jobs
        self.places = places        

        
    def web_scrapp_jobs_interface_run(self):

        for place in self.places:
            print ("searching jobs in {0}...".format(place))
            super().__init__(self.url, self.jobs, place)                 # Call inherited constructor method 





class Control(IODataHandler, FileManager):

    """ Control class, this class is trigger and data provider to other classes and methods."""
    
    def __init__(self, url, jobs, places):

        self.url = url
        self.jobs = jobs
        self.places = places
        self.visited = list()          # Track visited links, push correct direction on pagination case
        self.data = list()             # Holds collected data, once all url  data have traversed we will write this
                                       # list to a file

    def run(self):
        if self.jobs and self.places:
            self.initiate_file()
            self.web_scrapp_jobs_interface_run()
            self.save_data(self.data)
            return
        self.initiate_file(True)
            
            


# job webpage
url = "https://www.bika.net/poslovi/inozemstvo/"

# job locations
places = ['austrija', 'inozemstvo', 'nizozemska',
          'sjedinjene-americke-drzave', 'slovenija',
          'svicarska', 'belgija', 'irska', 'njemacka',
          'slovacka', 'svedska', 'ujedinjeno-kraljevstvo',]

# jobs titles
jobs = ['programer', 'softver', 'kuhar']


main = Control(url, jobs, places)
main.run()




