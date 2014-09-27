#global imports
import nose.tools
#local imports
from App.GetMovies import checkzip

class TestCheckZip():
    def test_get_location(self):
        passtest=checkzip.CheckZip(15232)
        location,error=passtest.get_location()
        nose.tools.assert_equal(error,False)
        nose.tools.assert_equal(location,'Pittsburgh, (PA) 15232')
        print location
        
        failtest=checkzip.CheckZip(00000)
        location,error=failtest.get_location()
        nose.tools.assert_equal(error,True)
        print location
        
        