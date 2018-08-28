-- initiate
-- drop table seoulBusData;

-- 서울 버스 노선에 대한 전체 정보를 저장하는 테이블
-- 중간에 에러가 나서 idx추가했는데 다른거 때문에 그랬엇는데 안없앴음 없애도 되는데 안없애도 될거같고 
create table seoulBusData(
    routeId varchar(10),
    routeName varchar(20),
    routeOrder varchar(4),
    sectionId varchar(10),
    stationId varchar(10),
    stationName varchar(200),
    xPos varchar(30),
    yPos varchar(30),
    primary key(routeId, stationId,routeOrder),
    index seoulbusidx (routeId, stationId, routeOrder)
)charset=utf8;

-- 서울 버스 노선ID 및 stationID에 해당하는 주말,공휴일 / 평일 이용객 비율
-- drop table ratioBusStationUser;
create table ratioBusStationUser(
    routeId varchar(10),
    stationId varchar(10),
    weekDayRideRatio int,
    weekDayAlightRatio int,
    weekendRideRatio int,
    weekendAlightRatio int,
    primary key(routeId, stationId),
    foreign key(routeId,stationId) 
        references seoulBusData(routeId,stationId),
    index ratioidx (routeId, stationId)
)charset=utf8;

-- 서울 버스의 월별 시간대별 이용객에 대한 정보를 저장하는 table
create table monthTimeBusUser(
    routeId varchar(10),
    stationId varchar(10),
    ride0 int,
    ride1 int,
    ride2 int,
    ride3 int,
    ride4 int,
    ride5 int,
    ride6 int,
    ride7 int,
    ride8 int,
    ride9 int,
    ride10 int,
    ride11 int,
    ride12 int,
    ride13 int,
    ride14 int,
    ride15 int,
    ride16 int,
    ride17 int,
    ride18 int,
    ride19 int,
    ride20 int,
    ride21 int,
    ride22 int,
    ride23 int,
    alight0 int,
    alight1 int,
    alight2 int,
    alight3 int,
    alight4 int,
    alight5 int,
    alight6 int,
    alight7 int,
    alight8 int,
    alight9 int,
    alight10 int,
    alight11 int,
    alight12 int,
    alight13 int,
    alight14 int,
    alight15 int,
    alight16 int,
    alight17 int,
    alight18 int,
    alight19 int,
    alight20 int,
    alight21 int,
    alight22 int,
    alight23 int,
    primary key(routeId, stationId),
    foreign key(routeId,stationId) 
        references seoulBusData(routeId,stationId),
    index mtuindex (routeId, stationId)
)charset = utf8;

