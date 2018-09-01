import pymysql
from xml.dom import minidom
from urllib.request import urlopen
from urllib.parse import urlencode, quote_plus, quote
from collections import OrderedDict
import json

'''
request : routeName,dayType, hour
response : busId, busName, busRoute with statistical data
    ride/alight statistical data is represented as intensity (0/1/2)
    0 is low, 2 is high


1. busCnt : 현재 운행중인 버스의 총 개수.
2. stCnt : 버스 노선의 정류장 개수.
3. upCnt : 그 시간대의 승차인원
4. downCnt : 그 시간대의 하차인원
5. p : 평일에 타는 승객 비율
6. weekdayCnt , weekendCnt

stCnt / busCnt  : 버스 사이에 정거장 개수
한 정거장 사이의 시간 : 약 1분 30초

시간당 탑승 인원
upCnt * p  / weekdayCnt

한 버스당 탑승 인원 유추
upCnt * p / weekdayCnt / ( 3600 / (90*stCnt/busCnt))
= upCnt * p  stCnt / (busCnt *40* weekdayCnt) 


얼마일때 적은 것이고 얼마일때 많은 것인가
'''

def makeStatsJson(routeNum, dayType, hour):
    # 반환할 json
    resultJson = OrderedDict()
    # mysql connect
    conn = pymysql.connect(host='localhost', user='gosituser', password='', db='gosit', charset='utf8')
    
    # set busName
    resultJson['busName'] = routeNum

    # find busId
    findBusIdsql = """ select distinct routeId, routeOrder from seoulbusdata where routeName=%s order by routeOrder"""
    with conn.cursor() as curs:
        curs.execute(findBusIdsql, (routeNum))
        resultJson['busId'] = ''
        for row in curs.fetchall():
            resultJson['busId'] = row[0]

    # can't find return 
    if resultJson['busId'] == '':
        resultJson["status"] = False
        return json.dumps(resultJson, ensure_ascii=False)

    # find busRoute
    resultJson['busRoute'] = []
    urlbase='http://210.96.13.82:8099/api/rest/busRouteInfo/getStaionByRoute.jsonp?busRouteId='
    url = urlbase + resultJson["busId"]
    urldata = urlopen(url)
    jsontext = urldata.read().decode('utf8')[5:-1]
    jsondata = json.loads(jsontext)

    # if no data , return
    if(jsondata['outStationByRoute']['msgHeader']['headerMsg'] == "결과가 없습니다."):
        print(routeNum)
        print('no result')
        f = open('./data/noRouteId.use', mode = 'a')
        f.write(routeNum +' no result\n')
        f.close()
        resultJson["status"] = False
        return json.dumps(resultJson, ensure_ascii=False)
    
    # to find busCount
    realtimeurlbase='http://210.96.13.82:8099/api/rest/buspos/getBusPosByRtid.jsonp?busRouteId='
    realtimeurl = realtimeurlbase + resultJson["busId"]
    realtimeurldata = urlopen(realtimeurl)
    realtimejsontext = realtimeurldata.read().decode('utf8')[5:-1]
    realtimejsondata = json.loads(realtimejsontext)
    
    # 정류장 총 개수
    staCount = len(jsondata['outStationByRoute']['msgBody']['itemList'])
    # 현재 운행중인 버스 대수
    busCount = len(realtimejsondata['outBusPosByRtid']['msgBody']['itemList'])

    # make resultJson['busRoute']
    # get statistical data
    for item in jsondata['outStationByRoute']['msgBody']['itemList']:
        routeDict = OrderedDict()
        routeDict['stationId'] = item['station']
        routeDict['stationName'] = item['stationNm']
        routeDict['arsId'] = item['arsId']
        routeDict['routeOrder'] = item['seq']
        
        # for get user number
        rideCntsql = "select sum(ride" + str(hour) + ") from monthtimebususer where routeId=%s and stationId = %s and routeOrder = %s"
        alightCntsql = "select sum(alight" + str(hour) + ") from monthtimebususer where routeId=%s and stationId = %s and routeOrder = %s"
        
        # ride number for hour, busId, stationId
        rideCnt = 0
        # alight number for hour, busId, stationId
        alightCnt = 0
        with conn.cursor() as curs:
            curs.execute(rideCntsql, (resultJson['busId'], routeDict['stationId'], routeDict['routeOrder']))
            for row in curs.fetchall():
                rideCnt = int(row[0])
            
            curs.execute(alightCntsql, (resultJson['busId'], routeDict['stationId'], routeDict['routeOrder']))
            for row in curs.fetchall():
                alightCnt = int(row[0])

        # for get ratio of weekday/weekend
        dayCntsql = "select sum(weekDayRideRatio),sum(weekDayAlightRatio),sum(weekendRideRatio),sum(weekendAlightRatio)  from ratiobusstationuser where routeId=%s and stationId = %s and routeOrder = %s"
        
        propRide = 0.0
        propAlight = 0.0
        with conn.cursor() as curs:
            curs.execute(dayCntsql,  (resultJson['busId'], routeDict['stationId'], routeDict['routeOrder']))
            weekdayRideCnt = 0
            weekdayAlightCnt = 0
            weekendRideCnt = 0
            weekendAlightCnt = 0
            for wd in curs.fetchall():
                weekdayRideCnt = int(wd[0])
                weekdayAlightCnt = int(wd[1])
                weekendRideCnt = int(wd[2])
                weekendAlightCnt = int(wd[3])

            if(dayType == 'weekday'):
                if(weekdayRideCnt+weekendRideCnt !=0):
                    propRide = weekdayRideCnt / (weekdayRideCnt + weekendRideCnt )
                if(weekdayAlightCnt+weekendAlightCnt !=0):
                    propAlight = weekdayAlightCnt / (weekdayAlightCnt+weekendAlightCnt)
            else:
                if(weekdayRideCnt+weekendRideCnt !=0):
                    propRide = weekendRideCnt / (weekdayRideCnt + weekendRideCnt)
                if(weekdayAlightCnt+weekendAlightCnt !=0):
                    propAlight = weekendAlightCnt / (weekdayAlightCnt+weekendAlightCnt)
            

        # num of weekday/weekend
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

        # get the result
        upRatio = 0.0
        downRatio = 0.0
        if dayType == 'weekday':
            upRatio = rideCnt * propRide *(staCount / busCount) / weekdayCnt / 40.0
            downRatio = alightCnt * propAlight *(staCount / busCount) / weekdayCnt /40.0
        else:    
            upRatio = rideCnt * propRide *(staCount / busCount) / weekendCnt / 40.0
            downRatio = alightCnt * propAlight *(staCount / busCount) / weekendCnt /40.0
        
        routeDict['up'] = upRatio
        routeDict['down'] = downRatio

        resultJson['busRoute'] +=[routeDict]
        

    return json.dumps(resultJson, ensure_ascii=False)

def stats(routeName, dayType, hour):
    json_data = makeStatsJson(routeName,dayType, hour)
    return json_data
