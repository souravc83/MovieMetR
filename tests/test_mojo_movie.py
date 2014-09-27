#global imports
import nose.tools
#local imports
from Scrapers import mojo_movie

class TestMojoMovie():
    def setup(self):
        self.mojomovie=mojo_movie.MojoMovie('Scrapers/movies2013.json')
    
    def testprocessmovie(self):
        self.mojomovie._read_jsonfile()
        self.mojomovie._list_of_dicts=[]
        for movielink in self.mojomovie._ordered_movie_dict:
            self.mojomovie._process_movie(movielink)
            break
        
        thisdict=self.mojomovie._list_of_dicts[0]
        
        for key in thisdict:
            print key,":",thisdict[key]
        return

    def test_getmoviedetails(self):
        pass
        #make sure there's a break condition 
        self.mojomovie.getmoviedetails()
        return
