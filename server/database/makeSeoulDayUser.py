import pymysql
from xml.dom import minidom
from urllib.request import urlopen
from urllib.parse import urlencode, quote_plus, quote

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

# bring the bus route id and name
with conn.cursor() as curs:
    sqlGetBusData = """select * from seoulbusdata"""
    curs.execute(sqlGetBusData)
    rs = curs.fetchall()
    for row in rs:
        busIdName.add((row[0], row[1]))

# 0,0 week day ride, 0,1 week day alight
# 1,0 weekend ride, 1,1 weekend alight
busDict = dict.fromkeys(busIdName, [[0,0],[0,0]])

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
            for bus in busIdName:
                ymd = year+month+day
                userqueryParams = ymd+'/'+quote(bus[1])+'/'
                try : 
                    getuserurl = urlopen(userUrl + userqueryParams)
                    dombus = minidom.parse(getuserurl)
                except:
                    print(userUrl+userqueryParams)
                    continue;

                rideList = [int(rpn.firstChild.data) for rpn in dombus.getElementsByTagName('RIDE_PASGR_NUM') if int(rpn.firstChild.data) >0]
                alightList = [int(apn.firstChild.data) for apn in dombus.getElementsByTagName('ALIGHT_PASGR_NUM') if int(apn.firstChild.data)>0]
                if (intday in holidays) or startTheDay%7==0 or startTheDay%7==6 :
                    busDict[bus][1][0] += sum(rideList)
                    busDict[bus][1][1] += sum(alightList)
                else :
                    busDict[bus][0][0] += sum(rideList)
                    busDict[bus][0][1] += sum(alightList)

            startTheDay+=1
            
# push data to database
with conn.cursor() as curs:
    sqlpushratio = """insert into ratioUser(routeId, routeName,weekDayRideRatio, weekDayAlightRatio,weekendRideRatio, weekendAlightRatio)
                 values (%s,%s, %s, %s, %s, %s) """
    for bus in busIdName:
        curs.execute(sqlpushratio, (bus[0], bus[1], busDict[bus][0][0], busDict[bus][0][1],busDict[bus][1][0],busDict[bus][1][1]))
conn.commit()
conn.close()