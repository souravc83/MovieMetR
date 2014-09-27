#global imports

#local imports
import mojo_movie
from process_moviedict_pickle import ProcessPickle
def main():
    #mojo=mojo_movie.MojoMovie('Scrapers/movies2013.json')
    #mojo.getmoviedetails()
    process_movie=ProcessPickle('dictlist.pickle')
    process_movie.process_pandas()

if __name__=="__main__":
    main()
    