#global imports

#local imports
from movietrainer import MovieTrainer

def traintest():
    trainer=MovieTrainer('dictlist_movies_2013.pickle','dictlist_movies_2014.pickle')
    trainer.explore_data()
    #trainer.train_2013()
    #trainer.test_2014()
    #trainer.save_db('current_movies.db')

if __name__=="__main__":
    traintest()