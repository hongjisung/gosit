import pymysql
from xml.dom import minidom
from urllib.request import urlopen
from urllib.parse import urlencode, quote_plus, quote
from collections import OrderedDict
import json

'''
initialcall request 에 따른 response json파일을 만들어 반환한다.
busName, busId, busRoute, rideWeekdayRatio, rideWeekendRatio정보를 시간별로 반환한다.

rideWeekdayRatio, rideWeekendRatio를 어떻게 구할 것인가(이용객이므로 승차만 고려)
버스에 대해서 db에서 평일/휴일 이용객 전체 수를 구한다.
버스에 대해서 db에서 시간대별 이용객 전체 수(1년간)를 구한다.
버스에 대해서 dayrecord.use에서 1년간 평일/휴일 개수를 구한다.

시간대별 평일 이용객 수
평일 전체 이용객 수 * (그 시간대 이용객 수/전체 이용객수) / 평일의 수 

시간대별 휴일 이용객 수
휴일 전체 이용객 수 * (그 시간대 이용객 수/전체 이용객수) / 휴일의 수 


'''

def makeJson(routeNum):
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

    resultJson["busRoute"] = []
    urlbase='http://210.96.13.82:8099/api/rest/busRouteInfo/getStaionByRoute.jsonp?busRouteId='
    
    url = urlbase + resultJson["busId"]
    urldata = urlopen(url)
    jsontext = urldata.read().decode('utf8')[5:-1]
    jsondata = json.loads(jsontext)
    if(jsondata['outStationByRoute']['msgHeader']['headerMsg'] == "결과가 없습니다."):
        print(routeNum)
        print('no result')
        f = open('./data/noRouteId.use', mode = 'a')
        f.write(routeNum +' no result\n')
        f.close()
        resultJson["status"] = False
        return json.dumps(resultJson, ensure_ascii=False)
    
    for item in jsondata['outStationByRoute']['msgBody']['itemList']:
        routedata = OrderedDict()
        routedata['index'] = item['seq']
        routedata['stationId'] = item['station']
        routedata['stationName'] = item['stationNm']
        routedata['arsId'] = item['arsId']
        resultJson['busRoute'] +=[routedata]


    resultJson["rideWeekdayRatio"] = []
    resultJson["rideWeekendRatio"] = []

    # weekday/ weekend total users
    weektotsql = """select sum(weekDayRideRatio),sum(weekendRideRatio) 
                    from ratiobusstationuser
                    where routeId = %s"""
    weekdaytotCnt = 0
    weekendtotCnt = 0
    with conn.cursor() as curs:
        curs.execute(weektotsql, resultJson['busId'])
        for row in curs.fetchall():
            weekdaytotCnt = int(row[0])
            weekendtotCnt = int(row[1])

    # the users for each time
    timeList = [str(i) for i in range(0,24)]
    timeusersql = "select "
    for t in timeList:
        timeusersql += "sum(ride"+t+")"
        if t!="23":
            timeusersql+=", "
    timeusersql += " from monthtimebususer where routeId = %s"
    timeuserCnt = []
    with conn.cursor() as curs:
        curs.execute(timeusersql, resultJson['busId'])
        for row in curs.fetchall():
            for i in range(24):
                timeuserCnt+=[int(row[i])]

    # the total users
    totuserCnt = sum(timeuserCnt)

    # the num of weekday/weekend
    weekdayCntsql = "select count(*) from dayType where kind='weekday'"
    weekendCntsql = "select count(*) from dayType where kind='weekend'"
    weekdayCnt = 0
    weekendCnt = 0
    with conn.cursor() as curs:
        curs.execute(weekdayCntsql)
        for wc in curs.fetchall():
            weekdayCnt =int(wc[0])
        curs.execute(weekendCntsql)
        for wc in curs.fetchall():
            weekendCnt = int(wc[0])

    for i in range(24):
        resultJson['rideWeekdayRatio'] +=[int(weekdaytotCnt*(timeuserCnt[i]/totuserCnt)/weekdayCnt)]
        resultJson['rideWeekendRatio'] +=[int(weekendtotCnt*(timeuserCnt[i]/totuserCnt)/weekendCnt)]
        


    return json.dumps(resultJson, ensure_ascii=False)

def initialCall(routeNum):
    json_data = makeJson(routeNum)
    return json_data