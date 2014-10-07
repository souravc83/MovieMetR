#global imports
from flask import Flask,render_template,request

#local imports
from GetMovies.getmovie import GetMovie


app = Flask(__name__)

def index(genre=None):
    movies=GetMovie(genre)
    movielist=movies.toptenmovies()
    return render_template('index.html',movielist=movielist)


@app.route('/')
@app.route('/index.html')
def mainpage():
    return index()


@app.route('/docu.html')
def docu():
    return index('Documentary')


@app.route('/foreign.html')
def foreign():
    return index('Foreign')
    
@app.route('/drama.html')
def drama():
    return index('Drama')

@app.route('/comedy.html')
def comedy():
    return index('Comedy')

@app.route('/thriller.html')
def thriller():
    return index('Thriller')

if __name__=="__main__":
    app.run(debug=True)
