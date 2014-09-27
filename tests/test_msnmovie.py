#global imports
import nose.tools
#local imports
from App.GetMovies import msnmovie

class TestMSNmovie():
    def test_getmovies(self):
        print "Pittsburgh movies:"
        msn1=msnmovie.MSNmovie()
        movielist=msn1.getmovielist()
        for movie in movielist:
            print movie,':',movielist[movie]

        print "SFO movies:"
        msn2=msnmovie.MSNmovie(94101)
        movielist=msn2.getmovielist()
        for movie in movielist:
            print movie,':',movielist[movie]
        

