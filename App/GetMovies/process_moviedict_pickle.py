#global imports
import pickle
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import re
from sklearn.linear_model import LinearRegression
#local imports

class ProcessPickle(object):
    
    def __init__(self,filename):
        self._pickle_filename=filename
        #to be defined later
        self._list_of_dicts=None
        self._dataframe=None
    
    def _load_dataframe(self):
        if os.path.isfile(self._pickle_filename) ==True:
            self._list_of_dicts=pickle.load(file(self._pickle_filename))
        else:
            print "Cannot find pickle file"
            return
            #raise error?
    
    def process_pandas(self):
        self._load_dataframe()
        self._dataframe=pd.DataFrame(self._list_of_dicts)
        
        #print self._dataframe.ix[105:110]
        #only_budget=self._dataframe[pd.isnull(self._dataframe["domestic_gross"])]
        #print len(only_budget.index)
        
        df_X=self._dataframe["theater_list"].values
        df_Y=self._dataframe["domestic_gross"].values
        
        theater_list=[]
        for i in range(df_X.shape[0]):
            
            
            if type(df_X[i])==list and len(df_X[i])>0:
                theater=df_X[i][0]
                theater=re.sub(',','',theater)
                theater=re.sub('-','0',theater)
                theater_list.append(int(theater))
                #theater_list.append(len(df_X[i]))
            else:
                theater_list.append(0)
        
        gross_list=df_Y.tolist()
        
        for i in range(len(gross_list)):
            gross_list[i]=int(gross_list[i])
        
        #df_X=df_X_list[:,0]
        #print len(df_X)
        #print len(df_Y)
        
        n_samples=len(theater_list)
        
        theater_arr=np.array(theater_list).reshape(n_samples,1)
        gross_arr=np.array(gross_list).reshape(n_samples,1)
        
        plt.plot(theater_list,gross_list,'bo')
        
        clf=LinearRegression()
        clf.fit(theater_arr,gross_arr)
        plt.plot(theater_arr,clf.predict(theater_arr),'r-',linewidth=2)
        
        plt.show()
        return
        
        