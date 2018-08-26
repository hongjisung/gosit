from xml.dom import minidom
from urllib.request import urlopen
from datetime import datetime
import pymysql

'''
request : bus route number , bus station id
send : predicated ride, alight user numbers
'''

# authentication key of data.seoul.go.kr
keyfile = open('./data/seoulAuthenticationKey.use')
authkey = keyfile.read()

# the day which can get from website 
# it depends on the site administer who update the data
yearmonth = '201708'
daysOfMonth = 31

# get this data from client , bus number and bus station id
busnum = '144'
busStationId = '107000063'

# url the number of bus users per month of given bus route number 
url = 'http://openapi.seoul.go.kr:8088/'+authkey.strip()+'/xml/CardBusTimeNew/1/200/'+yearmonth+'/'+busnum+'/'


time_dict = {0:'MIDNIGHT', 1:'ONE', 2:'TWO', 3:'THREE', 4:'FOUR', 5:'FIVE', 6:'SIX', 7:'SEVEN', 8:'EIGHT', 9:'NINE',\
    10:'TEN', 11:'ELEVEN', 12:'TWELVE', 13:'THIRTEEN', 14:'FOURTEEN', 15:'FIFTEEN', 16:'SIXTEEN', 17:'SEVENTEEN',\
    18: 'EIGHTEEN', 19:'NINETEEN', 20:'TWENTY', 21:'TWENTY_ONE', 22:'TWENTY_TWO', 23:'TWENTY_THREE'}
motion_dict = {'ride': 'RIDE_NUM', 'alight':'ALIGHT_NUM'}

# parse the xml of url 
dom = minidom.parse(urlopen(url))
dataByBusStop = dom.getElementsByTagName('row')

# show the bus user data of hour by the busnum and busstationid
for busstop in dataByBusStop:
    stdid = busstop.getElementsByTagName('STND_BSST_ID')
    if(stdid[0].firstChild.data != busStationId) :
        continue
    nowHour = datetime.today().hour
    print(nowHour)
    rideCount = time_dict[nowHour]+'_' +motion_dict['ride']
    alightCount = time_dict[nowHour]+'_'+motion_dict['alight']
    rideName = busstop.getElementsByTagName(rideCount)
    alightName = busstop.getElementsByTagName(alightCount)

    print('   number of ride in this hour: %.2f' % (int(rideName[0].firstChild.data)/float(daysOfMonth) ))
    print('   number of alight in this hour: %.2f'% (int(alightName[0].firstChild.data)/float(daysOfMonth) ))





