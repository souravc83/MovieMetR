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
        self._matchmovies()
        prediction_sorted=self._full_predicted_list.sort(columns=["prediction"],ascending=False)
        #print prediction_sorted.head()
        
        for index in prediction_sorted.index:
            [name,theaters,pred]=prediction_sorted.ix[index]
            topten.append([counter+1,name,theaters,pred])
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
           
           
           
        
        
        
