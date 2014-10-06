#global imports
import nose.tools
#local imports
from Scrapers import rotten_api

class TestRottenTomato():
    def setup(self):
        self.tomato=rotten_api.RottenTomato()
    
    def test_getmovielist(self):
        self.tomato._getmovielist()