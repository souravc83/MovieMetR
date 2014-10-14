#global imports
import sqlite3
import re
from nltk import word_tokenize
from nltk.corpus import stopwords
import string

class SearchMovie(object):
    """
    searches given text with movies from database and returns a match if one exists
    """
    def __init__(self,search_str):
        self._search_string=search_str
        self._db_filename="nowplaying.db"
        #tobe defined later
        self._token_dict=None
    
    def _get_all_movies(self):
        nowplaying_con=sqlite3.connect(self._db_filename)
        nowplaying_cursor=nowplaying_con.cursor()
        query1='SELECT \
                movieid,\
                moviename\
                FROM nowplaying'
        nowplaying_cursor.execute(query1)
        raw_moviedata=nowplaying_cursor.fetchall()
        self._token_dict=self._clean_and_tokenize(raw_moviedata)
    
    def _clean_token(self,txtstr):
        #stopset=set(stopwords.words('english')) #should we use standard stopwords
        stop = stopwords.words('english')
        exclude=set(string.punctuation)
        txtstr=''.join(ch for ch in txtstr if ch not in exclude)
        tokens=word_tokenize(txtstr)
        cleantoken=[token.lower() for token in tokens if token.lower() not in stop]
        return cleantoken
    
    def _clean_and_tokenize(self,raw_moviedata):
        token_dict={}
        for data in raw_moviedata:
            (movieid,name)=data
            name=name.encode('utf-8')
            name=re.sub('_',' ',name)
            token=self._clean_token(name)
            token_dict[movieid]=token
            
        return token_dict
    
    
    
    def _manip_actorstr(self,actorstr):
        if actorstr==None:
            return ''
        actorstr=re.sub('_',' ',actorstr)
        return actorstr
        
    
    def _get_target_movdict(self,target_id):
        query1='SELECT \
                moviename,\
                prediction,\
                score,\
                detailed,\
                movlink,\
                actor1,\
                actor2,\
                actor3\
                FROM nowplaying\
                WHERE\
                movieid=%s'%target_id
        nowplaying_con=sqlite3.connect(self._db_filename)
        nowplaying_cursor=nowplaying_con.cursor()
        nowplaying_cursor.execute(query1)
        raw_data=nowplaying_cursor.fetchall()
        
        (name,pred,audience_score,detailed,movlink,actor1,actor2,actor3)=raw_data[0]
        name=name.encode('utf-8')
        name=re.sub('_',' ',name)
        pred=pred*100
        pred=round(pred,1)
        actors=[self._manip_actorstr(actor1),\
                self._manip_actorstr(actor2),\
                self._manip_actorstr(actor3)]
        movdict={"name":name,\
                     "audience_score":audience_score,\
                     "prediction":pred,\
                      "movlink":movlink,\
                       "detailed":detailed,\
                       "actors":actors}
        return movdict
        
        
        
                
        
        
        
    def get_search_result(self):
        inputstr_tokens=self._clean_token(self._search_string)
        isSuccess=False
        target_movieid=None
        
        self._get_all_movies()
        
        #very inefficient, O(n), can this be improved?
                
        for movie_id in self._token_dict:
            
            if cmp(self._token_dict[movie_id],inputstr_tokens)==0:
                isSuccess=True
                target_movieid=movie_id
                break
        if isSuccess==True:
            movdict=self._get_target_movdict(target_movieid)
        else:
            movdict={}   
            
        return movdict,isSuccess
                
                
        
        
    