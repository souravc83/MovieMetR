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


@app.route('/',methods=['POST'])
@app.route('/index.html',methods=['POST'])
def index_zipcode():
    zipcode=request.form["zipcode"]
    is_zip_valid=CheckZip(zipcode)
    location,error=is_zip_valid.get_location()
    int_zip=15232#default
    if error==False:
        int_zip=int(zipcode)
    movies=GetMovie(int_zip)
    movielist=movies.toptenmovies()
    return render_template('index.html',movielist=movielist,location=location)
    
    

if __name__=="__main__":
    app.run(debug=True)
