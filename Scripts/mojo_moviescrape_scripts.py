#global imports

#local imports
import mojo_movie

def main():
    mojo=mojo_movie.MojoMovie('Scrapers/movies2013.json')
    mojo.getmoviedetails()
    