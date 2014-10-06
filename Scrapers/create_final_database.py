import sqlite3
import pandas as pd
import re

class FinalDB(object):
    """
    this class creates the final database by joining together
    two databases:
    1)the current movies database, which has all the movies released
    in 2014, and their corresponding prediction.
    2) the rotten tomatoes, "now playing" movies database
    
    We read both of them into pandas dataframes to make 
    string comparisons easier. SQL is limited in terms of
    sophisticated string comparisons
    """
    
    def __init__(self,prediction_db,rotten_db):
        self._rotten_db=rotten_db
        self._prediction_db=prediction_db
        
        self._nowplaying_db='nowplaying.db'
        #to be defined later
        self._matched_frame=None
        
    
    
        
    def _match_databases(self):
        #possible duplicate code, correct later
        
        #rotten dataframe
        
        rotten_con=sqlite3.connect(self._rotten_db)
        rotten_cursor=rotten_con.cursor()
        
        rotten_query='SELECT *\
                FROM rottentomatoes';
        rotten_cursor.execute(rotten_query)
        
        rotten_data=rotten_cursor.fetchall()
        
        rotten_df=pd.DataFrame(rotten_data,columns=["movieid","moviename","thumbnail","score"])
        rotten_df["moviename"]=rotten_df["moviename"].apply(lambda x:re.sub('\s','_',x))
        
        #prediction frame
        predict_con=sqlite3.connect(self._prediction_db)
        predict_cursor=predict_con.cursor()
        
        predict_query='SELECT *\
                FROM currentmovies';
        predict_cursor.execute(predict_query)
        
        predict_data=predict_cursor.fetchall()
        
        predict_df=pd.DataFrame(predict_data,columns=["moviename","prediction"])
        predict_df["moviename"]=predict_df["moviename"].apply(lambda x:re.sub('\s','_',x))
        
        #match the dataframes
        #need better string matching function here
        self._matched_frame=pd.merge(rotten_df,predict_df,on="moviename",how="inner")
        #print matched_frame.head()
        print len(self._matched_frame.index)
        
        #save as sql database
        nowplaying_con=sqlite3.connect(self._nowplaying_db)
        self._matched_frame.to_sql('nowplaying',nowplaying_con, if_exists='replace')
        

def main():
    predict_db='current_movies.db'
    rotten_db='rotten_intheaters.db'
    processed_db=FinalDB(predict_db,rotten_db)
    processed_db._match_databases()

if __name__=="__main__":
    main()
        
        
        
        
        
        
        
        
        
        
        
        
        
        