#global imports
import sqlite3
import pandas as pd
import re

#local imports
from msnmovie import MSNmovie

class GetMovie(object):
    """
    returns all the movies running in the theater now
    at a given location
    """

    def __init__(self,zipcode=None):
        self._zipcode=zipcode;
        self._localmovies=MSNmovie(zipcode=self._zipcode);
        self._db_filename="current_movies.db"
        self._moviedict=None;
        
        self._full_predicted_list=pd.DataFrame(columns=["moviename","theaters","prediction"])
        

    def _list_to_str(self, theaterlist):
        theaters=theaterlist[0]

        for i in range(1,len(theaterlist)):
            theaters=theaters+','+theaterlist[i]
            
        return theaters
        
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
        
    
    def _matchmovies(self):
        self._moviedict=self._localmovies.getmovielist()
        con=sqlite3.connect(self._db_filename)
        cursor=con.cursor()
        
        query1='SELECT *\
                FROM currentmovies';
        cursor.execute(query1)
        
        data1=cursor.fetchall()
        #for entry in data1:
            #print entry
        
        database_frame=pd.DataFrame(data1,columns=["moviename","prediction"])
        
        for index in database_frame.index:
            oldname=database_frame.loc[index]["moviename"]
            database_frame.loc[index,"moviename"]=re.sub(' ','',oldname)
       
        
        for movie in self._moviedict:
           
            mov_nospace=re.sub(' ','',movie)
            newframe=database_frame[database_frame["moviename"]==mov_nospace]
            
            if len(newframe.index):
                index=newframe.index[0]
                theaterstr=self._list_to_str(self._moviedict[movie])
                pred=newframe.ix[index]["prediction"]
                pred=round(pred,3)
                self._full_predicted_list.loc[len(self._full_predicted_list)+1]=\
                                                            [movie,theaterstr,pred]
                #print "Added: ",movie
    
    def _read_nowplaying(self):
        nowplaying_con=sqlite3.connect('nowplaying.db')
        nowplaying_cursor=nowplaying_con.cursor()
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
            
                
              
        
        
        
