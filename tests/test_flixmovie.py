#global imports
import nose.tools
#local imports
from App.GetMovies import flixstermovie

class TestMSNmovie():
    def test_scrapemainpage(self):
        flixmovie=flixstermovie.FlixMovie(15232)
        flixmovie._scrapemainpage()
        
    # def test_getmovies(self):
    #     print "Pittsburgh movies:"
    #     msn1=msnmovie.MSNmovie()
    #     movielist=msn1.getmovielist()
    #     for movie in movielist:
    #         print movie,':',movielist[movie]

        # print "SFO movies:"
        # msn2=msnmovie.MSNmovie(94101)
        # movielist=msn2.getmovielist()
        # for movie in movielist:
        #     print movie,':',movielist[movie]
        

