from xml.dom import minidom
import urllib2
from datetime import datetime

# authentication key of geonggi bus data
keyfile = open('./data/geonggiAuthenticationKey.use')
authkey = keyfile.read()

# get data from client
routeId = '233000007'
stationId = '200000078'

# openapi url of geonggi bus
url = 'http://openapi.gbis.go.kr/ws/rest/busarrivalservice/station?serviceKey=' + authkey.strip() +'&stationId='+stationId.strip()

# parse xml of url
dom = minidom.parse(urllib2.urlopen(url))
busList = dom.getElementsByTagName('busArrivalList')

for busdata in busList:
    busrouteList = busdata.getElementsByTagName('routeId')
    if(busrouteList[0].firstChild.data !=routeId):
        continue
    remainSeat1 = busdata.getElementsByTagName('reaminSearCnt1')
    remainSeat2= busdata.getElementsByTagName('reaminSearCnt2')
    


