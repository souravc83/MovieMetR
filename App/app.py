#global imports
from flask import Flask,render_template,request

#local imports
from GetMovies.getmovie import GetMovie
from GetMovies.moviesearch import SearchMovie


app = Flask(__name__)

def index(genre=None):
    movies=GetMovie(genre)
    movielist=movies.toptenmovies()
    return render_template('index.html',movielist=movielist)


@app.route('/')
@app.route('/index.html')
def mainpage():
    print "mainpage"
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

@app.route('/graph.html')
def graph():
    movies=GetMovie()
    movielist=movies.toptengraph()
    return render_template('graph.html',json_data=movielist)

@app.route('/',methods=['POST'])
@app.route('/index.html',methods=['POST'])
@app.route('/docu.html',methods=['POST'])
@app.route('/comedy.html',methods=['POST'])
@app.route('/drama.html',methods=['POST'])
@app.route('/thriller.html',methods=['POST'])
@app.route('/graph.html',methods=['POST'])
@app.route('/result.html',methods=['POST'])

def search():
    txtstr=request.form["address"]
    print "Here"
    print txtstr
    movsearch=SearchMovie(txtstr)
    movdict,isSuccess=movsearch.get_search_result()
    return render_template("result.html",movdict=movdict,isSuccess=isSuccess)



if __name__=="__main__":
    app.run(debug=True)
