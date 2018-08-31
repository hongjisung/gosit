import pymysql
from xml.dom import minidom
from urllib.request import urlopen
from urllib.parse import urlencode, quote_plus, quote
from collections import OrderedDict
import json

'''
버스 노선번호를 받아와 api를 이용하여 버스의 실시간위치정보를 반환한다.
'''
def makeLocJson(routeNum):
    resultJson = OrderedDict()
    conn = pymysql.connect(host='localhost', user='gosituser', password='', db='gosit', charset='utf8')
    
    numcheckSql = """select * from seoulBusData where routeName = %s """
    with conn.cursor() as curs:
        curs.execute("set names utf8")
        curs.execute(numcheckSql, (routeNum))
        if len(curs.fetchall()) == 0:
            resultJson["status"] = False
            return json.dumps(resultJson, ensure_ascii=False)        
        else:
            resultJson["status"] = True
            resultJson["busName"] = routeNum
            curs.execute(numcheckSql, (routeNum))
            for row in curs.fetchall():
                resultJson["busId"] = row[0]
    
    resultJson["location"] = []
    urlbase='http://210.96.13.82:8099/api/rest/buspos/getBusPosByRtid.jsonp?busRouteId='
    
    url = urlbase + resultJson["busId"]
    urldata = urlopen(url)
    jsontext = urldata.read().decode('utf8')[5:-1]
    jsondata = json.loads(jsontext)
    if(jsondata['outBusPosByRtid']['msgHeader']['headerMsg'] == "결과가 없습니다."):
        print(routeNum)
        print('no result')
        f = open('./data/noRouteId.use', mode = 'a')
        f.write(routeNum +' no result\n')
        f.close()
        resultJson['status'] = False
        return  json.dumps(resultJson, ensure_ascii=False)

    for item in jsondata['outBusPosByRtid']['msgBody']['itemList']:
        findstIdsql = """ select stationId from seoulbusdata where routeId = %s and sectionId = %s"""
        stationId = ''
        with conn.cursor() as curs2:
            curs2.execute(findstIdsql, (resultJson["busId"], item['sectionId']))
            for row2 in curs2.fetchall():
                stationId = row2[0]
        resultJson['location'] +=[stationId]

    return json.dumps(resultJson, ensure_ascii=False)

def realtimeLocation(routeNum):
    json_data = makeLocJson(routeNum)
    return json_data



