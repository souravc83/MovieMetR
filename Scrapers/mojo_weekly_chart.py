from bs4 import BeautifulSoup
from urllib2 import urlopen
import re


class WeeklyChart(object):
    """
    scrapes the weekly chart
    of a given movie and records the values
    """
    
    def __init__(self,newdict,weekly_url):
        self._newdict=newdict
        self._weekly_url=weekly_url
    
    def scrapechart(self):
        
        try:
            html_page=urlopen(self._weekly_url)
        except:
            print 'Could not open: '+self._weekly_url
            return
        
        #if try succeeds
        soup_page=BeautifulSoup(html_page,"lxml")
        all_tables=soup_page.find_all("table",{"class":"chart-wide"})
        
        #lists
        rank_list=[]
        weekly_gross_list=[]
        theater_list=[]
        dates_list=[]
        
        
        for table in all_tables:
            all_rows=table.find_all("tr")
            
            #skip first row,heading
            for i in range(1,len(all_rows)):
                all_cols=all_rows[i].find_all("td")
                #append to corresponding lists
                dates_list.append(all_cols[0].get_text().encode('utf-8'))
                rank_list.append(all_cols[1].get_text().encode('utf-8'))
                weekly_gross_list.append(self._extract_digits(\
                     all_cols[2].get_text().encode('utf-8')))
                theater_list.append(all_cols[4].get_text().encode('utf-8'))
        
        self._newdict["dates_list"]=dates_list
        self._newdict["weekly_gross_list"]=weekly_gross_list
        self._newdict["theater_list"]=theater_list
        self._newdict["rank_list"]=rank_list    
        #print dates_list
        #print weekly_gross_list
        #print theater_list
        #print rank_list
                
        return
        
    def _extract_digits(self,raw_str):
        #new_str=raw_str.encode('utf-8')
        pattern='(\d.+)'
        m=re.search(pattern,raw_str)
        result=m.group(0)
        result=re.sub(',','',result)
        return result
                
                
                
                
                

