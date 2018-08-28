from xml.dom import minidom
from urllib.request import urlopen
from urllib.parse import urlencode, quote_plus, quote
from datetime import datetime
import pymysql
from copy import deepcopy

'''
insert data to table monthTimeUser
save the user ride, alight data for each time about bus, station

'''

# connect to database
conn = pymysql.connect(host='localhost', user='gosituser', password='', db='gosit', charset='utf8')

# authentication key of data.seoul.go.kr
keyfile = open('../data/seoulAuthenticationKey.use')
authkey = keyfile.read()

# year and month
years = ['2017']
months = [str(i) for i in range(1,13)]

# get the routeId to search
busInfoList = set()
with conn.cursor() as curs:
    curs.execute('set names utf8')
    sql = """ select routeId, routeName from seoulBusData"""
    curs.execute(sql)
    for row in curs.fetchall():
        busInfoList.add((row[0], row[1]))

templist = [0 for i in range(48)]
# key is (routeId, stationId)
busDict = {}


# url the number of bus users per month of given bus route number 
urlbase = 'http://openapi.seoul.go.kr:8088/'+authkey.strip()+'/xml/CardBusTimeNew/1/200/'
    # +yearmonth+'/'+busnum+'/'

# tag name for xml parse
time_dict = {0:'MIDNIGHT', 1:'ONE', 2:'TWO', 3:'THREE', 4:'FOUR', 5:'FIVE', 6:'SIX', 7:'SEVEN', 8:'EIGHT', 9:'NINE',\
    10:'TEN', 11:'ELEVEN', 12:'TWELVE', 13:'THIRTEEN', 14:'FOURTEEN', 15:'FIFTEEN', 16:'SIXTEEN', 17:'SEVENTEEN',\
    18: 'EIGHTEEN', 19:'NINETEEN', 20:'TWENTY', 21:'TWENTY_ONE', 22:'TWENTY_TWO', 23:'TWENTY_THREE'}
motion_dict = {'ride': '_RIDE_NUM', 'alight':'_ALIGHT_NUM'}


# get data from api
for year in years:
    for month in months:
        ym = year+ '0' + month if len(month) < 2 else year+month
        print(ym)

        for busInfo in busInfoList:
            url = urlbase+ym+'/'+quote_plus(busInfo[1])+'/'
            try : 
                #print(url)
                dataxml = urlopen(url)
                dom = minidom.parse(dataxml)
                rowList = dom.getElementsByTagName('row')
                for row in rowList:
                    staId = row.getElementsByTagName('STND_BSST_ID')[0].firstChild.data
                    buskey = (busInfo[0], staId) 
                    for i in range(24):
                        ridetagname = time_dict[i] + motion_dict['ride']
                        rideuserdata = row.getElementsByTagName(ridetagname)[0].firstChild.data
                        alighttagname = time_dict[i] + motion_dict['alight']
                        alightuserdata = row.getElementsByTagName(alighttagname)[0].firstChild.data
                        if buskey in busDict.keys():
                            busDict[buskey][i] += int(rideuserdata)
                            busDict[buskey][i+24] += int(alightuserdata)
                        else : 
                            busDict[buskey] = deepcopy(templist)
                            busDict[buskey][i] += int(rideuserdata)
                            busDict[buskey][i+24] += int(alightuserdata)
            except :
                print(url)


# push data to database
with conn.cursor() as curs:
    curs.execute('set names utf8')
    sql = """insert into monthtimebususer values
            (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
            %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
            %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
            %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
            %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    for key in busDict.keys():
        insertdata = key + tuple(busDict[key])
        curs.execute(sql, insertdata)
    conn.commit()

#close sql connect
conn.close()








