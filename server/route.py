from flask import Flask, render_template,request
from flask import url_for, redirect, make_response
from flask_cors import CORS
import json
from src import initialBusCall, realtimeBusLocation
from src import statsBus, stationBusInfo


app = Flask(__name__)
CORS(app)


# initialCall protocol in ./develop_note/protocol.json
@app.route('/initialCall', methods=['POST','GET'])
def initialCall() :
    routeNum = 0
    if(request.method == 'POST'):
        routeNum = request.form['busName']
    else :
        routeNum = request.args.get('busName')
    json_data = initialBusCall.initialCall(routeNum)
    res = make_response(json_data)
    res.headers['Content-Type'] = 'initialCall/json'
    return res

# realtimeData protocol in ./develop_note/protocol.json
@app.route('/realtimeData', methods=['POST', 'GET'])
def realtimeLocation() : 
    routeNum = 0
    if(request.method == 'POST'):
        routeNum = request.form['busName']
    else :
        routeNum = request.args.get('busName')
    json_data = realtimeBusLocation.realtimeLocation(routeNum)
    res = make_response(json_data)
    res.headers['Content-Type'] = 'realtimeLoc/json'
    return res


# stats protocol in ./develop_note/protocol.json
@app.route('/stats', methods=['POST', 'GET'])
def stats() :
    routeName = '' 
    daytype = ''
    hour = 0
    if(request.method == 'POST'):
        routeName = request.form['busName']
        daytype = request.form['dayType']
        hour  = request.form['hour']
    else :
        routeName = request.args.get('busName')
        daytype = request.args.get('dayType')
        hour = request.args.get('hour')
    json_data = statsBus.stats(routeName,daytype, hour)
    res = make_response(json_data)
    res.headers['Content-Type'] = 'stats/json'
    return res

@app.route('/stationInfo', methods = ['POST', 'GET'])
def stationInfo():
    stationId = 0
    if(request.method == 'POST'):
        stationId = request.form['stationId']
    else :
        stationId = request.args.get('stationId')
    json_data = stationBusInfo.stationInfo(stationId)
    res = make_response(json_data)
    res.headers['Content-Type'] = 'stationInfo/json'
    return res; 

if __name__ == '__main__':
    app.run(host='0.0.0.0')    
