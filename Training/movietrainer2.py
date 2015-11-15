#global imports
from __future__ import division
import pickle
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import re
from sklearn.linear_model import LinearRegression
#import sklearn.linear_model as linear_model
from sklearn.cross_validation import train_test_split
from sklearn.cross_validation import KFold, cross_val_score
from sklearn.linear_model import LassoCV

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
    
    def _addtodict(self,name,this_dict):
        if this_dict.has_key(name):
            this_dict[name]+=1
        else:
            this_dict[name]=1
        return
        
    def _modify_string(self,playername):
        playername = re.sub('^\s+|\s+$','', playername)
        playername=re.sub('\s+','_',playername)
        playername=re.sub('\*','',playername)
        return playername
    
    #this function creates a list of features
    #corresponding to the most frequent actors 
    #in a movie
    def _create_playerdict(self,frame,colname,num_features):
        
        playerdict={}
        
        
        for index in frame.index:
            #for each row, we have list of actors
            #like ['Sandra Bullock', 'Melissa McCarthy']
            playerlist=frame.ix[index,colname] 
            
            
            if type(playerlist)!=float:
                #only actors have multiple list members, other players
                #like director don't
                if colname=="actors":
                    for playername in playerlist:
                        #remove spaces, *, leading trailing spaces
                        playername=self._modify_string(playername)
                        self._addtodict(playername,playerdict)

                else:
                    playerlist=self._modify_string(playerlist)
                    self._addtodict(playerlist,playerdict)   
        
        
        
        counter=0
        feature_list=[]
        #sort the dict to get players with highest number of movies
        for key,value in sorted(playerdict.items(),key=lambda x:x[1],reverse=True):
            #print key,value
            feature_list.append(key)
            counter+=1
            if counter>num_features:
                break
        return feature_list
    
    #this function returns a value of the player features for 
    #each movie
    
    def _create_player_features(self,frame,colname,num_features):
        #feature_list is all names of players with most movies
        feature_list=self._create_playerdict(frame,colname,num_features)
        actor_frame = pd.DataFrame()
        
        for player in feature_list:
            feature_name=colname+":"+player
            actor_frame[feature_name]=pd.Series(0,index=frame.index)
            bigplayer_name="feature:big_"+colname #TODO: take out of loop
            actor_frame[bigplayer_name]=pd.Series(0,index=frame.index)#big actors directors present or not?
            
        for index in frame.index:
            playerval=frame.ix[index,colname]
            if type(playerval)!=float: #playerval is not None
                if colname=="actors":
                    for actor in playerval:
                        actor=self._modify_string(actor)
                        if actor in feature_list:
                            thisfeature=colname+":"+actor
                            actor_frame.loc[index,thisfeature]=1
                else:
                    playerval=self._modify_string(playerval)
                    if playerval in feature_list:
                        thisfeature=colname+":"+playerval
                        actor_frame.loc[index,thisfeature]=1
                actor_frame.loc[index,bigplayer_name]=1
            else:
                actor_frame.loc[index,bigplayer_name]=0
                        
        return actor_frame
                        
                
        
    def _create_theater_features(self,frame):
        
        #add feature column
        theater_frame=pd.DataFrame()
        theater_frame["feature:num_theaters"]=pd.Series(0,index=frame.index)
        
        
        for index in frame.index:
            theater_list=frame.ix[index,"theater_list"]
            if type(theater_list)==list and len(theater_list)>0:
                theater=theater_list[0]
                theater=re.sub(',','',theater)
                if re.search('\d+',theater) is not None:
                    theater_frame.loc[index,"feature:num_theaters"]=int(theater)
                else:
                    theater_frame.loc[index,"feature:num_theaters"]=0
            else:
                theater_frame.loc[index,"feature:num_theaters"]=0
        
        return theater_frame
        
    def _first_weekend_rank(self,frame):
        #todo: try to merge with create theater features
        weekend_frame = pd.DataFrame()
        weekend_frame["feature:rank"]=pd.Series(0,index=frame.index)
        for index in frame.index:
            rank_list=frame.ix[index,"rank_list"]
            if type(rank_list)==list and len(rank_list)>0:
                rank=rank_list[0]
                rank=re.sub(',','',rank)
                if re.search('\d+',rank) is not None:
                    weekend_frame.loc[index,"feature:rank"]=int(rank)
                else:
                    weekend_frame.loc[index,"feature:rank"]=1000#some large number? or zero?
            else:
                weekend_frame.loc[index,"feature:rank"]=1000
        
        return weekend_frame
    
    def _create_running_time_feature(self,frame):
        runtime_frame = pd.DataFrame()
        runtime_frame["feature:runtime"]=pd.Series(0,index=frame.index)
        
        for index in frame.index:
            running_time=frame.ix[index,"runtime"]
            if type(running_time)!= float: #not NaN
                pattern='(\d+).+\s(\d+)'
                hrmin=re.match(pattern,running_time)
                if hrmin is not None:
                    hrs=hrmin.group(1)
                    mins=hrmin.group(2)
                    tot_time=int(hrs)*60+int(mins)
                    runtime_frame.loc[index,"feature:runtime"]=tot_time
                    
                else:
                    runtime_frame.loc[index,"feature:runtime"]=0
                    
            else:
                runtime_frame.loc[index,"feature:runtime"]=0
            
        return runtime_frame
                
    
    def _create_release_date_feature(self,frame):
        monthlist=["January","February","March","April","May","June"\
                "July","August","September","October","November","December"]
        month_frame = pd.DataFrame()
        for month in monthlist:
            feature_name="feature:release_"+month
            month_frame[feature_name]=pd.Series(0,index=frame.index) 
        
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
                        month_frame.loc[index,thisfeature]=1
        return month_frame
                        
                       
    
    def _extract_features(self,frame,isTraining=True):
        """
        extracts features from training and test frame
        all major data munging, cleaning takes place here
        
        """ 
        #pass
        #we will make clean_frame as the data frame, 
        #then we will define the training/test frame
        #and add each feature as a dataframe
        #and finally concatenate the features
    
                
        #check if labels exist for these movies 
        clean_data=frame[pd.notnull(frame["domestic_gross"])]
        
        list_of_frames=[]
        
        #no of theaters it opened at in the first week
        #keep this as first feature so that you can plot using this
        list_of_frames.append( self._create_theater_features(clean_data) )
        print "Created Theater Feature..."
        list_of_frames.append( self._first_weekend_rank(clean_data) )
        print "Created Rank Feature..."
        list_of_frames.append( self._create_running_time_feature(clean_data) )
        print "Created running time Feature..."
        list_of_frames.append( self._create_release_date_feature(clean_data) )
        print "Created release date Feature..."
        #create player features
        list_of_frames.append( \
                    self._create_player_features(clean_data,"actors",5) )
        list_of_frames.append( \
                    self._create_player_features(clean_data,"director",5) )
        list_of_frames.append( 
                    self._create_player_features(clean_data,"distributor",5) )
        list_of_frames.append( 
                    self._create_player_features(clean_data,"genre_toplist",5) )
        list_of_frames.append( 
                    self._create_player_features(clean_data,"mpaa_rating",5) )
        print "Created player Features..."
        
        #check dataframe shapes
        for frames in list_of_frames:
            assert frames.shape[0] == clean_data.shape[0]
            
        
        #concatenate the dataframes
        final_frame = pd.concat(list_of_frames,axis = 1)
        
        final_frame.to_csv("Training/training_frame.csv")
        
        #get training labels
        if isTraining == True:
            labels_arr=self._extract_labels(clean_data)
        else:
            prediction_frame=clean_data[["moviename","genre_toplist","actors"]]
       

        n_samples=len(final_frame.index)
        n_features=len(final_frame.columns)
        
        #from Dataframe to numpy array
        feature_arr=final_frame.values.reshape(n_samples,n_features)
        
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
        self._training_frame.to_csv("Training/raw_frame.csv")
        total_features,total_labels=self._extract_features(self._training_frame,isTraining=True)
        total_labels=np.ravel(total_labels)
        
        print type(total_features)
        print type(total_labels)

                                       
        
        
        #create train and test split
        self._features, test_features, self._labels, test_labels =\
            train_test_split(total_features, total_labels, test_size = 0.33)
        
        
        
        print self._features.shape
        print self._labels.shape
        print test_features.shape
        print test_labels.shape
        
        cv_outer = KFold(self._labels.shape[0],n_folds=5)
        self._clf = LassoCV(eps=0.01, n_alphas=10,cv =5)
        cross_val_arr=cross_val_score(self._clf,self._features,self._labels,cv=cv_outer)
        print "Finished Training....."
        
        r_sq=np.mean(cross_val_arr)
        print "R Square for training set: ",r_sq
        
        self._clf.fit(self._features,self._labels)
        plt.plot(test_labels, self._clf.predict(test_features),'ro',linewidth=2)
        plt.plot(np.arange(0,1.,.1),np.arange(0,1.,.1),'b-',linewidth=2)
        plt.xlabel("Actual Gross")
        plt.ylabel("Predicted Gross")
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




        
        
