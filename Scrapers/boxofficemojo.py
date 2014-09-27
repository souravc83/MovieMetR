from bs4 import BeautifulSoup
from urllib2 import urlopen
import re
import json
import time

class MovieWeekend(object):
    """
    this scrapes the weekend charts page from boxofficemojo.com
    """
    def __init__(self,year):
    
        self._baseurl='http://www.boxofficemojo.com/weekend/chart/?view=&';
        self._year=year;
        
        self._moviedict={}

        #to be defined later
        self._full_url=None;


    def _form_url(self,weekend):
        self._full_url=self._baseurl+'yr='+str(self._year)+'&wknd='+\
                  self._weekend_str(weekend)+'&p=.htm';
        return;

    def _weekend_str(self,weekend):
        if weekend<0:
            raise ValueError("weekend value negative:%d"%weekend)
        elif weekend<10:
            return '0'+str(weekend)
        elif weekend>53:
            raise ValueError("weekend exceeds maximum:%d"%weekend)
        else:
            return str(weekend)

    def _scrapeweekend(self,weekend):
        self._form_url(weekend)
        #print self._full_url
        html_page=urlopen(self._full_url)
        soup_page=BeautifulSoup(html_page,"lxml");
        all_rows=soup_page.find_all("tr");

        for movierow in all_rows:
            all_columns=movierow.find_all("td")
            for column in all_columns:
                try:
                    movie_col=column.a["href"]
                    #print movie_col
                    if re.match('^/movies/',movie_col) is not None:
                        movie_name=column.a.get_text();
                        
                        if movie_col not in self._moviedict:
                            self._moviedict[movie_col]=movie_name
                        
                        #print movie_name
                except:
                    continue
        return

    def scrapemain(self):
        for i in range(1,53):
            try:
                self._scrapeweekend(i);
                time.sleep(5)
                print "Week: "+str(i)
            except:
                continue
        return
    
    def savejson(self,filename):
        with open(filename,'w') as outfile:
            json.dump(self._moviedict,outfile,indent=4)
        return;


def main():
    mojo=MovieWeekend(2013)
    mojo.scrapemain()
    mojo.savejson('movies2013.json')

if __name__ == "__main__":
    main()
               
