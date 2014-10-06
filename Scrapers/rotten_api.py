from __future__ import division
from urllib2 import urlopen
import json
import math
import time
import sqlite3

class RottenTomato(object):
    """
    this class returns a list of now playing movies from rottentomatoes
    """
    
    def __init__(self,API_KEY='s3jrdjk599zxk5u42uracq45'):
        self._API_KEY=API_KEY
        
        self._in_theaters_url=('http://api.rottentomatoes.com/api/public/'
                               'v1.0/lists/movies/in_theaters.json?apikey=')+self._API_KEY
        
        self._database_name='rotten_intheaters.db'
        
    
    def _getmovielist(self):
        full_url=self._in_theaters_url
        response=urlopen(full_url).read()
        response_json=json.loads(response)
        
        tot_pages=int(math.ceil(response_json["total"]/16))
        
        #for protection when it comes back to the same page
        movieid_dict={}
        
        
        for pageno in range(tot_pages):
            time.sleep(5)
            full_url=self._in_theaters_url+'&page='+str(pageno+1)
            response=urlopen(full_url).read()
            response_json=json.loads(response)
            movielist=response_json["movies"]
        
            for movie in movielist:
                movieid=movie["id"]
                moviename=movie["title"]
                thumbnail=movie["posters"]["thumbnail"]
                audience_score=movie["ratings"]["audience_score"]
                if movieid in movieid_dict:
                    break
                else:
                    movieid_dict[movieid]=True
                    
                print moviename,":",thumbnail,":",audience_score
                self._cursor.execute('INSERT INTO rottentomatoes\
                                      VALUES(?,?,?,?)'\
                                      ,(movieid,moviename,thumbnail,audience_score))
        return
    
    def _init_database(self):
        self._con=sqlite3.connect(self._database_name)
        self._cursor=self._con.cursor()
        self._cursor.execute('DROP TABLE IF EXISTS rottentomatoes')
        self._cursor.execute('CREATE TABLE rottentomatoes(\
                                           movieid INT PRIMARY KEY NOT NULL,\
                                           moviename VARCHAR(255) NOT NULL,\
                                           thumbnail VARCHAR(255),\
                                           score INT)')
        return
    
    def read_currentmovies(self):
        self._init_database()
        self._getmovielist()
        self._con.commit()
        self._con.close()
        return

def main():
    tomato=RottenTomato()
    tomato.read_currentmovies()

if __name__=="__main__":
    main()