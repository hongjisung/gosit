import pymysql
from xml.dom import minidom
from urllib.request import urlopen
from urllib.parse import urlencode, quote_plus, quote
from copy import deepcopy

'''
서울 버스 노선 및 정류장의 일별 승하차 인원을 이용하여
평일 / 주말,공휴일의 사용자 비율을 알아낸다.

'''

# 인증키 open
dayauthkey = open('../data/breakdayAuthenticationKey.use').read()
userAuthKey = open('../data/seoulDayAuthenticationKey.use').read()

# 공통 url
dayUrl = 'http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getRestDeInfo'
pageNo = '1'
totalCount ='30'
userUrl = 'http://openapi.seoul.go.kr:8088/'+userAuthKey.strip() \
    +'/xml/CardBusStatisticsServiceNew/1/100/'


# 날짜 정보
years = ['2017']
months = [i for i in range(1,13)]
# 윤달 무시
days = [31,28,31,30,31,30,31,31,30,31,30,31]

#MySqL connection
conn = pymysql.connect(host='localhost', user='gosituser', password='', db='gosit', charset='utf8')

# bus route id and name 
busIdName = set()
busStation = set()

# bring the bus route id and name
with conn.cursor() as curs:
    curs.execute("set names utf8")
    sqlGetBusData = """select * from seoulbusdata"""
    curs.execute(sqlGetBusData)
    rs = curs.fetchall()
    for row in rs:
        busIdName.add((row[0], row[1]))
        busStation.add((row[0], row[1], row[4],row[5]))

# 0,0 week day ride, 0,1 week day alight
# 1,0 weekend ride, 1,1 weekend alight
inputlist = [[0,0],[0,0]]

busDict = dict()
for bus in busStation:
    busDict[bus] = deepcopy(inputlist)
print(len(busIdName))


# get bus route number users per day
startTheDay = 0
for year in years:
    for intmonth in months:
        month = '0' + str(intmonth) if(intmonth<10)  else str(intmonth)
        print(month)
        dayqueryParams = '?' + 'ServiceKey=' +dayauthkey.strip() + '&solYear=' +year+'&solMonth='+month
        getdayurl = urlopen(dayUrl+dayqueryParams)
        dom = minidom.parse(getdayurl)
        holidayList = dom.getElementsByTagName('locdate')
        holidays = [int(hdl.firstChild.data[-2:]) for hdl in holidayList]

        print(holidays)
        for intday in range(1, days[intmonth-1]+1):
            day = '0'+str(intday) if (intday<10)  else str(intday)
            print(year+month+day)
            ymd = year+month+day

            # start from not done 
            if(ymd<='20170101') :
                startTheDay+=1
                continue
            

            # record the number of users from url
            
            for bus in busIdName:
                userqueryParams = ymd+'/'+quote(bus[1])+'/'
                try : 
                    getuserurl = urlopen(userUrl + userqueryParams)
                    dombus = minidom.parse(getuserurl)
                except:
                    print(userUrl+userqueryParams)
                    continue

                rideList = [int(rpn.firstChild.data) for rpn in dombus.getElementsByTagName('RIDE_PASGR_NUM')]
                alightList = [int(apn.firstChild.data) for apn in dombus.getElementsByTagName('ALIGHT_PASGR_NUM') ]
                staIdList = [rpn.firstChild.data for rpn in dombus.getElementsByTagName('STND_BSST_ID') ]
                staNameList = [rpn.firstChild.data for rpn in dombus.getElementsByTagName('BUS_STA_NM') ]
                
                for i in range(len(staIdList)):
                    busst = (bus[0],bus[1],staIdList[i], staNameList[i])
                    if( busst not in busStation):
                        continue;
                    if (intday in holidays) or startTheDay%7==0 or startTheDay%7==6 :
                        # update sql so += => =
                        busDict[busst][1][0] = rideList[i]
                        busDict[busst][1][1] = alightList[i]
                    else :
                        busDict[busst][0][0] = rideList[i]
                        busDict[busst][0][1] = alightList[i]
            
            # each day save the record to database
            with conn.cursor() as curs:
                curs.execute("set names utf8")
                sqlselect = """select count(*) from ratioBusStationuser """
                curs.execute(sqlselect)
                # insert sql if the table is empty
                if curs.fetchall()[0][0] == 0:
                    curs2 = conn.cursor()
                    sqlpushratio = """insert into ratioBusStationUser(routeId, routeName,stationId, stationName,weekDayRideRatio, weekDayAlightRatio,weekendRideRatio, weekendAlightRatio)
                                values (%s,%s, %s, %s, %s, %s,%s,%s) """
                    for bus in busStation:
                        curs2.execute(sqlpushratio, (bus[0], bus[1], bus[2],bus[3],busDict[bus][0][0], busDict[bus][0][1],busDict[bus][1][0],busDict[bus][1][1]))
                    conn.commit()
                # update sql if the table if full
                else :
                    curs2 = conn.cursor()
                    sqlupdate = """update ratioBusStationUser 
                                set weekDayRideRatio = %s, weekDayAlightRatio = %s, weekendRideRatio = %s, weekendAlightRatio = %s
                                where routeId = %s, stationId = %s"""
                    sqlgetdata ="""select * from ratioBusStationuser where routeId = %s and stationId = %s"""
                    for bus in busIdName:
                        curs2.execute(sqlgetdata, (bus[0], bus[2]))
                        fourdata = [i for i in curs2.fetchall()[0][4:]]
                        curs2.execute(sqlupdate, (fourdata[0] + busDict[bus][0][0], \
                                                fourdata[1] + busDict[bus][0][1],
                                                fourdata[2] + busDict[bus][1][0],
                                                fourdata[3] + busDict[bus][1][1],
                                                bus[0],
                                                bus[2]))
                    conn.commit()

            
            # record about the registered day
            # file for record about the days registered to db
            dayrecord = open('../data/dayrecord2.use', mode = 'a')
            
            if (intday in holidays) or startTheDay%7==0 or startTheDay%7==6 :
                dayrecord.write(ymd+' weekend\n')
            else :
                dayrecord.write(ymd+' weekday\n')
            # close file
            dayrecord.close()


            startTheDay+=1
            
# close connect sql
conn.close()
