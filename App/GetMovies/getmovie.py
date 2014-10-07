#global imports
import sqlite3
import re


class GetMovie(object):
    """
    returns all the movies running in the theater now
    at a given location
    """

    def __init__(self,genre=None):
        self._db_filename="current_movies.db"
        self._moviedict=None;
        self._genre=genre
        
    def toptenmovies(self):
        
        counter=0;
        topten=[]
        self._read_nowplaying()
        
        
        for data in self._moviedata:
            (name,thumbnail,pred)=data
            name=name.encode('utf-8')
            name=re.sub('_',' ',name)
            thumbnail=thumbnail.encode('utf-8')
            pred=round(pred,3)
            pred_percent=pred*100
            topten.append([counter+1,name,thumbnail,pred,pred_percent])
            counter+=1
            if counter==10:
                break
        
        return topten
        
        
    def _read_nowplaying(self):
        nowplaying_con=sqlite3.connect('nowplaying.db')
        nowplaying_cursor=nowplaying_con.cursor()
        if self._genre is not None:
            query1='SELECT \
                    moviename,\
                    thumbnail,\
                    prediction\
                    FROM nowplaying\
                    WHERE genre=\'%s\'\
                    ORDER BY prediction DESC\
                    LIMIT 10 '%self._genre
        else:
            query1='SELECT \
                    moviename,\
                    thumbnail,\
                    prediction\
                    FROM nowplaying\
                    ORDER BY prediction DESC\
                    LIMIT 10 '
            
        nowplaying_cursor.execute(query1)
        self._moviedata=nowplaying_cursor.fetchall()
        
        #for data in self._moviedata:
        #    print data
            
                
              
        
        
        
