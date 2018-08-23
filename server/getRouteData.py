import pymysql
import json
from collections import OrderedDict
from flask import Flask, request, url_for, redirect, make_response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

"""
request : bus route number
response : bus station data of route (station name, station id)

http get method
url : localhost:5000/busRoute?routeNum={routeNum}

"""

#MySqL connection

def sendRouteJson(routeNum):
    conn = pymysql.connect(host='localhost', user='gosituser', password='', db='gosit', charset='utf8')
    resultJson = OrderedDict()
    with conn.cursor() as curs:
        curs.execute("set names utf8")
        sql = """select * from seoulbusdata where routeName = %s order by routeOrder ASC"""
        curs.execute(sql, (routeNum))
        for row in curs.fetchall():
            stationInfo = OrderedDict()
            stationInfo["routeId"] = row[0]
            stationInfo["routeName"] = row[1]
            stationInfo["routeOrder"] = row[2]
            stationInfo["sectionId"] = row[3]
            stationInfo["stationId"] = row[4]
            stationInfo["stationName"] = row[5]
            stationInfo["xPos"] = row[6]
            stationInfo["yPos"] = row[7]
            resultJson[row[2]] = stationInfo
    conn.close()
    return json.dumps(resultJson, ensure_ascii=False)


# get route number from client
# name is routeNum
@app.route('/busRoute', methods=['POST','GET'])
def busRoute():
    routeNum = 0
    if(request.method == 'POST') :
        routeNum = request.form['routeNum']
    else :
        routeNum = request.args.get('routeNum')
    
    json_data = sendRouteJson(routeNum)
    res = make_response(json_data)
    res.headers['Content-Type'] = 'busRoute'
    return res

if __name__ == '__main__':
    app.run(debug=True)



