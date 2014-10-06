from bs4 import BeautifulSoup
import urllib2


#http://igoogle.flixster.com/igoogle/showtimes?movie=all&date=20141006&postal=15232&submit=Go

#http://www.nytimes.com/movies/showtimes.html?zipcode=15232&submit.x=14&submit.y=6&submit=Search

"""
Uses the flixster igoogle app to scrape for movie showtimes at a zipcode
"""

class FlixMovie(object):
    def __init__(self,zipcode=None):
        self._baseurl='http://www.google.co.in/movies?near=Pittsburgh,PA'
        if zipcode==None:
            self._zipcode=15232;#default
        else:
            self._zipcode=zipcode;#check zipcode
        #to be defined later
        self._full_url=None;
        self._movielist={};
    def _scrapemainpage(self):
        self._full_url=self._baseurl;
        hdr = {'User-Agent': 'Mozilla/5.0'}
        req = urllib2.Request(self._full_url,headers=hdr)
        html_page=urllib2.urlopen(req)
        soup_page=BeautifulSoup(html_page,"lxml");
        
        all_theater_page=soup_page.find_all("div",{"class":"theater"})
        
        print len(all_theater_page)

        for theater_page in all_theater_page:
            desc=theater_page.find("div",{"class":"desc"})
            theater_name=desc.find("a").get_text().encode('utf-8')
            #print theater_name
            showtimes=theater_page.find("div",{"class":"showtimes"})
            all_movies=showtimes.find_all("div",{"class":"movie"})
            
            for thismovie in all_movies:
                moviename=thismovie.find("div",{"class":"name"}).get_text().encode('utf-8')
                print moviename
                if moviename not in self._movielist:
                    self._movielist[moviename]=[theater_name]
                else:
                    self._movielist[moviename].append(theater_name);
                    
    def getmovielist(self):
        self._scrapemainpage()
        return self._movielist