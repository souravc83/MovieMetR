#global import
from bs4 import BeautifulSoup
from urllib2 import urlopen
import re
import sqlite3
#local import

class ZipDir(object):
    """
    scrapes zipcodedirectory.com
    for all zipcodes of America, and corresponding towns
    """
    
    def __init__(self):
        self._baseurl='http://www.zipcodesdirectory.com'
        self._database_name='us_zipcodes.db'
        #to be defined later
        self._con=None
        self._cursor=None
    
    def scrape(self):
        self._init_database()
        self._scrapestates()
    
    def _scrapestates(self):
        html_page=urlopen(self._baseurl)
        soup_page=BeautifulSoup(html_page,"lxml")
        table=soup_page.find("table")
        all_cols=table.find_all("td")
        
        for col in all_cols:
            coltext=col.get_text()
            pattern=re.compile('(\(..\))')
            abbr=pattern.search(coltext)
            state_abbr= abbr.group(0).encode('utf-8')
            statelink=col.find("a")["href"]
            self._eachstate(statelink,state_abbr)
            print "Completed: ",state_abbr
            #break
        self._con.commit()
        self._con.close()
        return
    
    def _eachstate(self,statelink,state_abbr):
        stateurl=self._baseurl+'/'+statelink
        html_page=urlopen(stateurl)
        soup_page=BeautifulSoup(html_page,"lxml")
        
        table=soup_page.find("table")
        
        all_rows=table.find_all("tr")
        
        for row in all_rows:
            cols=row.find_all("td")
            zipcode=cols[0].get_text()
            city=cols[1].get_text().encode('utf-8')
            if len(zipcode)==5:
                #print zipcode, city
                zip_int=int(zipcode)
                
                self._cursor.execute('INSERT INTO uszipcodes\
                                      VALUES(?,?,?)'\
                                      ,(zip_int,city,state_abbr))
        
        return
    
    def _init_database(self):
        self._con=sqlite3.connect(self._database_name)
        self._cursor=self._con.cursor()
        self._cursor.execute('DROP TABLE IF EXISTS uszipcodes')
        self._cursor.execute('CREATE TABLE uszipcodes(\
                                           zipcode INT PRIMARY KEY NOT NULL,\
                                           city VARCHAR(255) NOT NULL,\
                                           state VARCHAR(2) NOT NULL)')
                                            
        
        


def main():
    myzipdir=ZipDir()
    myzipdir.scrape()

if __name__=="__main__":
    main()
    
        
    