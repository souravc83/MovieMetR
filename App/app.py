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
    moviedict=movies.toptenmovies()
    return render_template('index.html',moviedict=moviedict,zipcode=15232)


@app.route('/',methods=['POST'])
@app.route('/index.html',methods=['POST'])
def index_zipcode():
    zipcode=request.form["zipcode"]
    is_zip_valid=CheckZip(zipcode)
    location,error=check_zipcode.get_location()
    movies=GetMovie()
    moviedict=movies.toptenmovies()
    return render_template('index.html',moviedict=moviedict,location=location)
    
    

if __name__=="__main__":
    app.run(debug=True)
