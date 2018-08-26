import pymysql
import json
from collections import OrderedDict



"""
return bus route data by json 
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


def busRoute(routeNum):
    json_data = sendRouteJson(routeNum)
    return json_data




