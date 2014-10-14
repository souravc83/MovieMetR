#global imports
from flask import Flask,render_template,request,jsonify


app=Flask(__name__)

@app.route('/')
@app.route('/index.html')
def index():
    
    dataset=[{"x":5,"y":10,"name":"one"},
             {"x":10,"y":20,"name":"two"},
             {"x":15,"y":30,"name":"three"},
             {"x":20,"y":40,"name":"four"}
             ]
    
    #dataset=[[5,10,"one"],[10,20,"two"],[15,30,"three"],[20,40,"four"]]
    #dataset_json=[jsonify(val) for val in dataset]

    
    return render_template('index.html',json_data=dataset)

if __name__=="__main__":
    app.run(debug=True)