from bs4 import BeautifulSoup
from urllib2 import urlopen


class MSNmovie(object):
    def __init__(self,zipcode=None):
        self._baseurl='http://movies.msn.com/showtimes/showtimes.aspx?shloc='
        if zipcode==None:
            self._zipcode=15232;#default
        else:
            self._zipcode=zipcode;#check zipcode
        #to be defined later
        self._full_url=None;
        self._movielist={};
        
        
    def _scrapemainpage(self):
        self._full_url=self._baseurl+str(self._zipcode);
        html_page=urlopen(self._full_url)
        soup_page=BeautifulSoup(html_page,"lxml");
        
        all_theater_page=soup_page.find_all("div",{"class":"st_TheaterRoot"})

        for theater_page in all_theater_page:
            theater_name=theater_page.find("div",\
            {"class":"st_TheaterName"}).get_text().encode('utf-8');
            
            for moviediv in theater_page.find_all("div",\
            {"class":"st_MovieInfo"}):
                moviename=moviediv.get_text().encode('utf-8');
                if moviename not in self._movielist:
                    self._movielist[moviename]=[theater_name]
                else:
                    self._movielist[moviename].append(theater_name);
                    
    def getmovielist(self):
        self._scrapemainpage()
        return self._movielist

    
    #todo
    #1. go to each movie link and save movie detail
    #including rotten tomato rating and reviews
    #2. rel. database between theaters and movies
    
    
#def main():
#    msn1=MSNmovie();
#    movielist=msn1.getmovielist()
#    for movie in movielist:
#        print movie,':',movielist[movie]
#    return;

#if __name__ == "__main__":
#    main()
        
