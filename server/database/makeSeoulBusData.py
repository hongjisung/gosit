import pandas as pd 
import pymysql
'''
problem with unicode we should use python3 here
'''

# the data file for push database
seoulBusFile = pd.rxead_csv('../data/seoulBusData.csv', dtype=str)

#MySqL connection
conn = pymysql.connect(host='localhost', user='gosituser', password='', db='gosit', charset='utf8')

# create cursor
curs = conn.cursor()

# Sql query
sql = """insert into 
        seoulBusData(routeId, routeName , routeOrder , sectionId ,stationId ,stationName ,xPos,yPos) 
        values(%s, %s, %s, %s, %s, %s, %s, %s)"""

for idx in seoulBusFile.index:
    print(tuple(seoulBusFile.iloc[idx]))
    curs.execute(sql, tuple(seoulBusFile.iloc[idx]))
conn.commit()
conn.close()