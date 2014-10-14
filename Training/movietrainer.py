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
    
    def _addtodict(self,name,dict):
        if name in dict:
            dict[name]+=1
        else:
            dict[name]=1
        return
        
    def _modify_string(self,playername):
        playername=re.sub('\s','_',playername)
        playername=re.sub('\*','',playername)
        return playername
    
    def _create_playerdict(self,frame,colname,num_features):
        
        playerdict={}
        
        
        for index in frame.index:
            playerlist=frame.ix[index,colname]
            
            
            if type(playerlist)!=float:
                if colname=="actors":
                    for playername in playerlist:
                        playername=self._modify_string(playername)
                        self._addtodict(playername,playerdict)

                else:
                    playerlist=self._modify_string(playerlist)
                    self._addtodict(playerlist,playerdict)   
        
        
        
        counter=0
        feature_list=[]
        for key,value in sorted(playerdict.items(),key=lambda x:x[1],reverse=True):
            #print key,value
            feature_list.append(key)
            counter+=1
            if counter>num_features:
                break
        return feature_list
    
    def _create_player_features(self,frame,colname,num_features):
        feature_list=self._create_playerdict(frame,colname,num_features)
        
        for player in feature_list:
            feature_name=colname+":"+player
            frame[feature_name]=pd.Series(0,index=frame.index)
            bigplayer_name="feature:big_"+colname
            frame[bigplayer_name]=pd.Series(0,index=frame.index)#big actors directors present or not?
            
        for index in frame.index:
            playerval=frame.ix[index,colname]
            if type(playerval)!=float: #playerval is not None
                if colname=="actors":
                    for actor in playerval:
                        actor=self._modify_string(actor)
                        if actor in feature_list:
                            thisfeature=colname+":"+actor
                            frame.loc[index,thisfeature]=1
                else:
                    playerval=self._modify_string(playerval)
                    if playerval in feature_list:
                        thisfeature=colname+":"+playerval
                        frame.loc[index,thisfeature]=1
                frame.loc[index,bigplayer_name]=1
            else:
                frame.loc[index,bigplayer_name]=0
                        
        return 
                        
                
        
    def _create_theater_features(self,frame):
        
        #add feature column
        frame["feature:num_theaters"]=pd.Series(0,index=frame.index)
        
        
        for index in frame.index:
            theater_list=frame.ix[index,"theater_list"]
            if type(theater_list)==list and len(theater_list)>0:
                theater=theater_list[0]
                theater=re.sub(',','',theater)
                if re.search('\d+',theater) is not None:
                    frame.loc[index,"feature:num_theaters"]=int(theater)
                else:
                    frame.loc[index,"feature:num_theaters"]=0
            else:
                frame.loc[index,"feature:num_theaters"]=0
        
        return
        
    def _first_weekend_rank(self,frame):
        #todo: try to merge with create theater features
        frame["feature:rank"]=pd.Series(0,index=frame.index)
        for index in frame.index:
            rank_list=frame.ix[index,"rank_list"]
            if type(rank_list)==list and len(rank_list)>0:
                rank=rank_list[0]
                rank=re.sub(',','',rank)
                if re.search('\d+',rank) is not None:
                    frame.loc[index,"feature:rank"]=int(rank)
                else:
                    frame.loc[index,"feature:rank"]=1000#some large number? or zero?
            else:
                frame.loc[index,"feature:rank"]=1000
        
        return
    
    def _create_running_time_feature(self,frame):
        frame["feature:runtime"]=pd.Series(0,index=frame.index)
        
        for index in frame.index:
            running_time=frame.ix[index,"runtime"]
            if type(running_time)!= float: #not NaN
                pattern='(\d+).+\s(\d+)'
                hrmin=re.match(pattern,running_time)
                if hrmin is not None:
                    hrs=hrmin.group(1)
                    mins=hrmin.group(2)
                    tot_time=int(hrs)*60+int(mins)
                    frame.loc[index,"feature:runtime"]=tot_time
                    
                else:
                    frame.loc[index,"feature:runtime"]=0
                    
            else:
                frame.loc[index,"feature:runtime"]=0
            
        return
                
    
    def _create_release_date_feature(self,frame):
        monthlist=["January","February","March","April","May","June"\
                "July","August","September","October","November","December"]
        
        for month in monthlist:
            feature_name="feature:release_"+month
            frame[feature_name]=pd.Series(0,index=frame.index) 
        
        for index in frame.index:
            release_date=frame.ix[index,"release_date"]
            if type(release_date)!=float:
                pattern='(\S+)\s(\d+)'
                monthday=re.match(pattern,release_date)
                if monthday is not None:
                    month=monthday.group(1)
                    day=monthday.group(2)
                    
                    if month in monthlist:
                        thisfeature="feature:release_"+month
                        frame.loc[index,thisfeature]=1
        return
                        
                       
    
    def _extract_features(self,frame,isTraining=True):
        """
        extracts features from training and test frame
        all major data munging, cleaning takes place here
        
        """ 
        pass
        #we will make features as the training frame, add feature columns
        #and then remove original columns
        #then we don't have to worry about which movies we dropped
        
         
        cols_to_remove=(frame.columns).tolist()
        
        #check if labels exist for these movies 
        features=frame[pd.notnull(frame["domestic_gross"])]
        
        #no of theaters it opened at in the first week
        #keep this as first feature so that you can plot using this
        self._create_theater_features(features)
        print "Created Theater Feature..."
        #self._first_weekend_rank(features)
        print "Created Rank Feature..."
        #self._create_running_time_feature(features)
        print "Created running time Feature..."
        self._create_release_date_feature(features)
        print "Created release date Feature..."
        #create player features
        self._create_player_features(features,"actors",20)
        #self._create_player_features(features,"director",20)
        #self._create_player_features(features,"distributor",20)
        #self._create_player_features(features,"genre_toplist",5)
        #self._create_player_features(features,"mpaa_rating",5)
        print "Created player Features..."
        
        
    

        
        
        #get training labels
        if isTraining == True:
            labels_arr=self._extract_labels(features)
        else:
            prediction_frame=features[["moviename","genre_toplist","actors"]]
       
        
        
        
        #remove all original cols
        features.drop(cols_to_remove,axis=1,inplace=True)
        n_samples=len(features.index)
        n_features=len(features.columns)
        
        feature_arr=features.values.reshape(n_samples,n_features)
        
        print "Created All Features....."
        
        if isTraining is True:
            return feature_arr,labels_arr
        else:
            return feature_arr,prediction_frame

        
        #plt.plot(theater_arr,self._clf.predict(theater_arr),'r-',linewidth=2)
        
        #plt.show()
        return
    
    def _extract_labels(self,frame):
        
        df_Y=frame["domestic_gross"].values
        gross_list=df_Y.tolist()
        for i in range(len(gross_list)):
            gross_list[i]=int(gross_list[i])
        
        max_gross=np.max(gross_list)
        #print max_gross
        gross_list=[x/max_gross for x in gross_list]
        n_samples=len(gross_list)
        gross_arr=np.array(gross_list).reshape(n_samples,1)
        
        return gross_arr
        
    def _get_top_actors(self,actorlist):
        top_actors=[None,None,None]
        if type(actorlist) ==float:
            return top_actors;
        
        counter=0
        for actor in actorlist:
            top_actors[counter]=self._modify_string(actor)
            counter+=1
            if counter==2:
                break
        return top_actors
                
                
             
        
    def explore_data(self):
        """
        plots and prints various kinds of stuff to test out the data
        change, comment and uncomment here directly
        """
        if self._training_frame is None:
            self._load_dataframe()
        
        
        #col_list.remove('actors')
        #print col_list
        #self._training_frame.drop(col_list,axis=1,inplace=True)
        
        #print self._training_frame.ix[500:510]
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
    
    def top_5_genres(self):
        if self._training_frame is None:
            self._load_dataframe()
        genre_list=self._create_playerdict(self._training_frame,"genre_toplist",5)
        print genre_list
        
    
    
    def train_2013(self):
        #pass
        self._load_dataframe()
        self._features,self._labels=self._extract_features(self._training_frame,isTraining=True)
        
        self._clf=LinearRegression()
        self._clf.fit(self._features,self._labels)
        print "Finished Training....."
        
        r_sq=self._clf.score(self._features,self._labels)
        print "R Square for training set: ",r_sq
        
        plt.plot(self._features[:,0],self._labels,'bo')
        plt.plot(self._features[:,0],self._clf.predict(self._features),'ro',linewidth=2)
        plt.show()
        
    
    def test_2014(self):
        #check if already trained
        if self._clf is None:
            self.train_2013()
        
        print "Generating Test Features..."
        self._test_features,self._prediction_frame=self._extract_features(\
                                           self._test_frame,isTraining=False)
        
        self._prediction_frame["prediction"]=self._clf.predict(self._test_features)
        print "Finished Testing..."
        
        #sanity check and normalize
        self._prediction_frame["prediction"]=self._prediction_frame["prediction"].apply(\
                                             lambda x: 0 if x<0 else x)
        maxpred=self._prediction_frame["prediction"].max()
        if maxpred>1:
            self._prediction_frame["prediction"]=self._prediction_frame["prediction"].apply(\
                                                 lambda x: x/maxpred)
            
        
        
        print self._prediction_frame.head()
        
        
        
        
    
    def save_db(self,filename):
        con=sqlite3.connect(filename)
        cursor=con.cursor()
        cursor.execute('DROP TABLE IF EXISTS currentmovies')
        cursor.execute('CREATE TABLE currentmovies(\
                                     moviename VARCHAR(255) ,\
                                     genre VARCHAR(255),\
                                     prediction INT,\
                                     actor1 VARCHAR(255),\
                                     actor2 VARCHAR(255),\
                                     actor3 VARCHAR(255))')
        
        for index in self._prediction_frame.index:
            movname=self._prediction_frame.ix[index]["moviename"].encode('utf-8')
            pred=self._prediction_frame.ix[index]["prediction"]
            genre=self._prediction_frame.ix[index]["genre_toplist"].encode('utf-8')
            (actor1,actor2,actor3)=self._get_top_actors(self._prediction_frame.ix[index]["actors"])
            if type(movname)==float and math.isnan(movname)==True:
                continue
            print movname,genre,pred
            
            cursor.execute('INSERT INTO currentmovies\
                             VALUES(?,?,?,?,?,?)',(movname,genre,pred,actor1,actor2,actor3))
        
        con.commit()
        con.close()


#running_time




        
        
