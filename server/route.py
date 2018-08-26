from flask import Flask, render_template,request
from flask import url_for, redirect, make_response
from flask_cors import CORS
import json
from src.getRouteData import busRoute

app = Flask(__name__)
CORS(app)

# get route number from client
# name is routeNum
@app.route('/busRoute', methods=['POST','GET'])
def findBusRoute():
    routeNum = 0
    if(request.method == 'POST') :
        routeNum = request.form['routeNum']
    else :
        routeNum = request.args.get('routeNum')
    json_data = busRoute(routeNum)
    res = make_response(json_data)
    res.headers['Content-Type'] = 'findBusRoute/json'
    return res

if __name__ == '__main__':
    app.run()    
