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
    urlbase = 'http://ws.bus.go.kr/api/rest/buspos/getBusPosByRtid?ServiceKey='
    key = open('./data/realtimeBusAuthKey.use').read().strip()
    option = '&busRouteId='

    resultJson = OrderedDict()
    resultJson["busName"] = routeNum
    conn = pymysql.connect(host='localhost', user='gosituser', password='', db='gosit', charset='utf8')
    with conn.cursor() as curs:
        sql = """ select * from seoulbusdata where routeName = %s"""
        curs.execute(sql, (routeNum))
        for row in curs.fetchall():
            busRouteId = row[0]
            resultJson["busId"] = busRouteId
            resultJson["location"] = []

            url = urlbase+key+option+busRouteId
            realtimeurl = urlopen(url)
            dom = minidom.parse(realtimeurl)
            nowLocs = [nl.firstChild.data for nl in dom.getElementsByTagName('sectionId')]
            curs2 = conn.cursor()
            sql2 = """ select * from seoulbusdata where routeId = %s and sectionId = %s"""
            for staId in nowLocs:
                curs2.execute(sql2, (busRouteId, staId))
                
                for bsdata in curs2.fetchall():
                    if len(bsdata) >4:
                        resultJson["location"] += [bsdata[4]]

            break

    return json.dumps(resultJson, ensure_ascii=False)

def realtimeLocation(routeNum):
    json_data = makeLocJson(routeNum)
    return json_data



