#global imports
import nose.tools
#local imports
from Scrapers import mojo_weekly_chart

class TestWeeklyChart:
    
    def setup(self):
        self.weekly_url='http://www.boxofficemojo.com/movies/?page=weekly&id=hydepark.htm'
        emptydict={}
        self.chart=mojo_weekly_chart.WeeklyChart(emptydict,self.weekly_url)
    
    def testscrapechart(self):
        self.chart.scrapechart()
        return
