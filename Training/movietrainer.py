#global imports
from __future__ import division
import pickle
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import re
from sklearn.linear_model import LinearRegression
import sqlite3
import math
#local imports

class MovieTrainer(object):
    
    def __init__(self,training_file,test_file):
        self._training_pickle=training_file
        self._test_pickle=test_file
        
        #to be defined later
        self._list_of_dicts=None
        self._dataframe=None
        self._features=None
        self._test_features=None
        self._labels=None
        self._clf=None
        
        self._training_frame=None
        self._test_frame=None
        self._prediction_frame=None
        
        #dicts
        self._actor_dict=None
        self._director_dict=None
        self._genre_dict=None
        self._production_house=None
        
    
    def _load_dataframe(self):
        if os.path.isfile(self._training_pickle) ==True:
            self._training_dict=pickle.load(file(self._training_pickle))
        else:
            raise AttributeError("Cannot find pickle file:%s"%self._training_pickle)
        
        if os.path.isfile(self._test_pickle) ==True:
            self._test_dict=pickle.load(file(self._test_pickle))
        else:
           raise AttributeError("Cannot find pickle file:%s"%self._test_pickle)
          
         #load pandas frame
         
        self._training_frame=pd.DataFrame(self._training_dict)
        self._test_frame=pd.DataFrame(self._test_dict)
        
        #drop movies with no names 
        self._training_frame.dropna(subset=["moviename"])
        self._test_frame.dropna(subset=["moviename"])
        return
            #raise error?
    
    def _extract_features(self,frame,istraining=True):
        """
        extracts features from training and test frame
        all major data munging, cleaning takes place here
        
        """ 
        
        #check if labels exist for these movies      
        bool_series=pd.notnull(frame["domestic_gross"])
        
        df_X=frame["theater_list"].values
        
        
        
        #print type(df_X1)
        #print df_X1.head()
        
        theater_list=[]
        for i in range(df_X.shape[0]):
            if bool_series.ix[i]==True and type(df_X[i])==list and len(df_X[i])>0:
                theater=df_X[i][0]
                theater=re.sub(',','',theater)
                if re.search('\d+',theater) is not None:
                    theater_list.append(int(theater))
                else:
                    bool_series.ix[i]=False
                #theater_list.append(len(df_X[i]))
            else:
                bool_series.ix[i]=False
        
        
        n_samples=len(theater_list)
        
        theater_arr=np.array(theater_list).reshape(n_samples,1)
        return theater_arr,bool_series

        
        #plt.plot(theater_arr,self._clf.predict(theater_arr),'r-',linewidth=2)
        
        #plt.show()
        return
    
    def _extract_labels(self,frame,bool_series):
        
        df_Y=(frame[bool_series])["domestic_gross"].values
        gross_list=df_Y.tolist()
        for i in range(len(gross_list)):
            gross_list[i]=int(gross_list[i])
        
        max_gross=np.max(gross_list)
        #print max_gross
        gross_list=[x/max_gross for x in gross_list]
        
        n_samples=len(gross_list)
        gross_arr=np.array(gross_list).reshape(n_samples,1)
        return gross_arr
        
        
        
    def explore_data(self):
        """
        plots and prints various kinds of stuff to test out the data
        change, comment and uncomment here directly
        """
        if self._training_frame is None:
            self._load_dataframe()
        
        #print self._training_frame.ix[5:10]
        #print len(self._training_frame.index)
        #only_budget=self._training_frame[pd.isnull(self._training_frame["domestic_gross"])]
        #print len(only_budget.index)
        
        #actors_there=self._training_frame[pd.notnull(self._training_frame["actors"])]
        #print len(actors_there.index)
        #print actors_there.head()
        
        #director_there=self._training_frame[pd.notnull(self._training_frame["director"])]
        #print len(director_there.index)
        #print director_there.head()
        pass
        
    def train_2013(self):
        #pass
        self._load_dataframe()
        self._features,bool_series=self._extract_features(self._training_frame)
        self._labels=self._extract_labels(self._training_frame,bool_series)
        self._clf=LinearRegression()
        self._clf.fit(self._features,self._labels)
        
        plt.plot(self._features,self._labels,'bo')
        plt.plot(self._features,self._clf.predict(self._features),'r-',linewidth=2)
        plt.show()
        
    
    def test_2014(self):
        #check if already trained
        if self._clf is None:
            self.train_2013()
        self._test_features,bool_series=self._extract_features(self._test_frame)
        self._prediction_frame=(self._test_frame[bool_series])["moviename"]
        self._prediction_frame=pd.DataFrame(self._prediction_frame)
        
        self._prediction_frame["prediction"]=1.0
        
        
        print type(self._test_features)
        for i in range(len(self._prediction_frame.index)):
            self._prediction_frame.ix[i,"prediction"]=\
                            self._clf.predict(self._test_features[i])
        
        print self._prediction_frame.head()
        
        
        
        
    
    def save_db(self,filename):
        con=sqlite3.connect(filename)
        cursor=con.cursor()
        cursor.execute('DROP TABLE IF EXISTS currentmovies')
        cursor.execute('CREATE TABLE currentmovies(\
                                     moviename VARCHAR(255) ,\
                                     prediction INT)')
        
        for index in self._prediction_frame.index:
            movname=self._prediction_frame.ix[index]["moviename"]
            pred=self._prediction_frame.ix[index]["prediction"]
            if type(movname)==float and math.isnan(movname)==True:
                continue
            print movname,pred
            
            cursor.execute('INSERT INTO currentmovies\
                             VALUES(?,?)',(movname.encode('utf-8'),pred))
        
        con.commit()
        con.close()


#running_time
#genre (one-hot)
#MPAA rating (one hot)
#actors
#production house (one hot)



        
        
