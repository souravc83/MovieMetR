#global imports
import nose.tools
#local imports
from Training import movietrainer

class TestMovieTrainer():
    def setup(self):
        self.trainer=movietrainer.MovieTrainer('dictlist_movies_2013.pickle','dictlist_movies_2014.pickle')
        self.trainer._load_dataframe()
        
    def test_playerdict(self):
        
        actorlist=self.trainer._create_playerdict(self.trainer._training_frame,"actors",10)
        print actorlist
        dist_list=self.trainer._create_playerdict(self.trainer._training_frame,"distributor",10)
        print dist_list
    
    def test_create_player_features(self):
        
        self.trainer._create_player_features(self.trainer._training_frame,"distributor",10)
        self.trainer._create_player_features(self.trainer._training_frame,"actors",10)
        print self.trainer._training_frame.ix[500:510,["moviename","distributor","distributor:Buena_Vista"]]
        print self.trainer._training_frame.ix[500:510,["moviename","actors","actors:James_Franco"]]
    
    def test_create_running_time_feature(self):
        self.trainer._create_running_time_feature(self.trainer._training_frame)
        print self.trainer._training_frame.ix[500:510,["moviename","runtime","feature:runtime"]]
    
    def test_create_release_date_feature(self):
        self.trainer._create_release_date_feature(self.trainer._training_frame)
        col_list=["moviename","release_date"]
        monthlist=["January","February","March","April","May","June"\
                "July","August","September","October","November","December"]
        for month in monthlist:
            feature_name="feature:release_"+month
            col_list.append(feature_name)
        print self.trainer._training_frame.ix[500:510,col_list]
        