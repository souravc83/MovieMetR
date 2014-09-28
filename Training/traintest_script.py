#global imports

#local imports
from movietrainer import MovieTrainer

def traintest():
    trainer=MovieTrainer('dictlist.pickle','dictlist_movies_2014.pickle')
    trainer.train_2013()
    trainer.test_2014()
    trainer.save_db('current_movies.db')

if __name__=="__main__":
    traintest()