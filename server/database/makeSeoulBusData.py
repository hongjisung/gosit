import pandas as pd 
import pymysql
from xml.dom import minidom
from urllib.request import urlopen
from urllib.parse import urlencode, quote_plus, quote
from copy import deepcopy
import json

'''
problem with unicode we should use python3 here
'''

# the data file for push database
seoulBusFile = pd.read_csv('../data/seoulBusData.csv', dtype=str)


#MySqL connection
conn = pymysql.connect(host='localhost', user='gosituser', password='', db='gosit', charset='utf8')

# create cursor
curs = conn.cursor()

# Sql query
sql = """insert into 
        seoulBusData(routeId, routeName , routeOrder , sectionId ,stationId ,stationName ,arsId) 
        values(%s, %s, %s, %s, %s, %s, %s)"""

# route data url
urlbase='http://210.96.13.82:8099/api/rest/busRouteInfo/getStaionByRoute.jsonp?busRouteId='

for busRouteID in seoulBusFile.노선ID.unique():
    url = urlbase+busRouteID
    urldata = urlopen(url)
    jsontext = urldata.read().decode('utf8')[5:-1]
    jsondata = json.loads(jsontext)
    if(jsondata['outStationByRoute']['msgHeader']['headerMsg'] == "결과가 없습니다."):
        print(busRouteID)
        print('no result')
        f = open('../data/noRouteId.use', mode = 'a')
        f.write(busRouteID +' no result\n')
        f.close()
        continue
    
    for row in jsondata['outStationByRoute']['msgBody']['itemList']:
        insertValue = (row['busRouteId'],row['busRouteNm'],\
            row['seq'],row['section'],row['station'],row['stationNm'],row['arsId'])
        with conn.cursor() as curs:
            curs.execute(sql, insertValue)

    

conn.commit()
conn.close()