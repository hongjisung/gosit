import pymysql

conn = pymysql.connect(host='localhost', user='gosituser', password='', db='gosit', charset='utf8')
dayInfo = open('../data/dayrecord.use')
sql = """insert into dayType values (%s, %s)"""

with conn.cursor() as curs:
    while True:
        data = dayInfo.readline()
        if not data: break
        curs.execute(sql, (data[:8], data[-8:-1]))
    conn.commit()
conn.close()    
