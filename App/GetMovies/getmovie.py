#global imports
import sqlite3
import re


class GetMovie(object):
    """
    returns all the movies running in the theater now
    at a given location
    """

    def __init__(self,genre=None):
        self._db_filename="current_movies.db" #change this to nowplaying.db?
        self._moviedict=None;
        self._genre=genre
        
    def toptenmovies(self):
        
        counter=0;
        topten=[]
        self._read_nowplaying()
        
        
        for data in self._moviedata:
            movdict={"index":data["index"],\
                     "name":data["name"],\
                     "thumbnail":data["thumbnail"],\
                     "movlink":data["movlink"],\
                     "prediction":data["prediction"],\
                      "actors":data["actors"]}
            topten.append(movdict)
            counter+=1
            if counter==10:
                break
        
        return topten
    
    def _manip_actorstr(self,actorstr):
        if actorstr==None:
            return ''
        actorstr=re.sub('_',' ',actorstr)
        return actorstr
    
    def _clean_moviedata(self,input_data):
        
        movielist=[]
        counter=0
        for data in input_data:
            (name,thumbnail,pred,score,movlink,actor1,actor2,actor3)=data
            #clean name
            name=name.encode('utf-8')
            name=re.sub('_',' ',name)
            thumbnail=thumbnail.encode('utf-8')
            #clean prediction
            pred=pred*100
            pred=round(pred,1)
            
            actors=[self._manip_actorstr(actor1),\
                    self._manip_actorstr(actor2),\
                    self._manip_actorstr(actor3)]
            
            
            movdict={"index":counter+1,\
                     "name":name,\
                     "thumbnail":thumbnail,\
                     "movlink":movlink,\
                     "prediction":pred,\
                     "audience_score":score,\
                     "actors":actors}
            movielist.append(movdict)
            counter+=1
            
        return movielist
               
        
    def _read_nowplaying(self):
        nowplaying_con=sqlite3.connect('nowplaying.db')
        nowplaying_cursor=nowplaying_con.cursor()
        if self._genre is not None:
            query1='SELECT \
                    moviename,\
                    thumbnail,\
                    prediction,\
                    score,\
                    movlink,\
                    actor1,\
                    actor2,\
                    actor3\
                    FROM nowplaying\
                    WHERE genre=\'%s\'\
                    ORDER BY prediction DESC\
                    LIMIT 10 '%self._genre
        else:
            query1='SELECT \
                    moviename,\
                    thumbnail,\
                    prediction,\
                    score,\
                    movlink,\
                    actor1,\
                    actor2,\
                    actor3\
                    FROM nowplaying\
                    ORDER BY prediction DESC\
                    LIMIT 10 '
            
        nowplaying_cursor.execute(query1)
        raw_moviedata=nowplaying_cursor.fetchall()
        self._moviedata=self._clean_moviedata(raw_moviedata)
        
        #for data in self._moviedata:
        #    print data
    def toptengraph(self):
        """
        top ten movies in a json format for the /graph.html page
        """
                
        counter=0
        topten=[]
        self._read_nowplaying()
        for data in self._moviedata:
            movdict={"name":data["name"],\
                     "audience_score":data["audience_score"],\
                     "prediction":data["prediction"]}
            topten.append(movdict)
            counter+=1
            if counter==10:
                break
        return topten              
        
        
        
