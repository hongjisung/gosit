-- initiate
--drop table seoulBusData;

서울 버스 노선에 대한 전체 정보를 저장하는 테이블
중간에 에러가 나서 idx추가했는데 다른거 때문에 그랬엇는데 안없앴음 없애도 되는데 안없애도 될거같고 
create table seoulBusData(
    routeId varchar(10),
    routeName varchar(20),
    routeOrder varchar(4),
    sectionId varchar(10),
    stationId varchar(10),
    stationName varchar(200),
    xPos varchar(30),
    yPos varchar(30),
    idx int auto_increment,
    primary key(idx)
)charset=utf8;

-- 서울 버스 노선ID 및 stationID에 해당하는 주말,공휴일 / 평일 이용객 비율
-- initiate
-- drop table ratioUser;

create table ratioUser(
    routeId varchar(10),
    routeName varchar(20),
    weekDayRideRatio int,
    weekDayAlightRatio int,
    weekendRideRatio int,
    weekendAlightRatio int,
    primary key(routeId),
    index ratioidx (routeId)
)charset=utf8;


