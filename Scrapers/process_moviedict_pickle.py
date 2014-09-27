#global imports
import pickle
import pandas as pd
import os

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
        
        print self._dataframe.ix[105:110]
        return
        
        