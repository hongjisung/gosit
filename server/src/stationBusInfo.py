import pymysql
from xml.dom import minidom
from urllib.request import urlopen
from urllib.parse import urlencode, quote_plus, quote
from collections import OrderedDict
import json

'''
버스 정류장 Id를 받아와 그 정류장에 도착할 버스 정보를 반환한다.
'''
def makeStaInfoJson(stationId):
    resultJson = OrderedDict()
    resultJson['stationId'] = stationId
    conn = pymysql.connect(host='localhost', user='gosituser', password='', db='gosit', charset='utf8')
    key = open('./data/busarrivekey.txt').read().strip()
    urlbase = 'http://ws.bus.go.kr/api/rest/arrive/getArrInfoByRouteAll?serviceKey='

    routeIdList = []
    with conn.cursor() as curs:
        sql = """select routeId from seoulbusdata where stationId = %s"""
        curs.execute(sql, (stationId))
        for row in curs.fetchall():
            routeIdList +=[row[0]]

    resultJson['arrivalBusInfo'] = []
    for routeId in routeIdList:
        url = urlbase + key + '&busRouteId=' + routeId
        stateurl = urlopen(url)
        dom = minidom.parse(stateurl)

        for item in dom.getElementsByTagName('itemList'):
            stid = [ i.firstChild.data for i in item.getElementsByTagName('stId')]
            if(stid[0] != stationId):
                continue
            arr1 = [ i.firstChild.data for i in item.getElementsByTagName('arrmsg1')]
            arr2 = [ i.firstChild.data for i in item.getElementsByTagName('arrmsg2')]
            businfo = OrderedDict()
            businfo['routeId'] = routeId
            businfo['firstBefoBusInfo'] = arr1[0]
            businfo['secondBefoBusInfo'] = arr2[0]
            resultJson['arrivalBusInfo'] += [businfo]



    return json.dumps(resultJson, ensure_ascii=False)

def stationInfo(stationId):
    json_data = makeStaInfoJson(stationId)
    return json_data


