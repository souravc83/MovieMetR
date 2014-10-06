#global imports
from flask import Flask,render_template,request

#local imports
from GetMovies.getmovie import GetMovie
from GetMovies.checkzip import CheckZip


app = Flask(__name__)


@app.route('/')
@app.route('/index.html')
def index():
    movies=GetMovie()
    movielist=movies.toptenmovies()
    return render_template('index.html',movielist=movielist,zipcode=15232)


if __name__=="__main__":
    app.run(debug=True)
