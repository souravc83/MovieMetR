#global imports
import nose.tools
#local imports
from App.GetMovies import getmovie

class TestGetMovie():
    def test_get_movie(self):
        localmovies=getmovie.GetMovie()
        movlist=localmovies.toptenmovies()
        print len(movlist)
        for entry in movlist:
            print entry
        
        