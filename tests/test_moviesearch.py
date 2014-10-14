#global imports
import nose.tools
#local imports
from App.GetMovies import moviesearch

class TestSearchMovie():
    def test_searchmovie(self):
        movies=moviesearch.SearchMovie('guardians of the galaxy')
        mdict,isSuccess=movies.get_search_result()
        
        print mdict
        return
        
        
        