-- initiate
-- 서울 버스 노선에 대한 전체 정보를 저장하는 테이블
create table seoulBusData(
    routeId varchar(10),
    routeName varchar(20),
    routeOrder int,
    sectionId varchar(10),
    stationId varchar(10),
    stationName varchar(200),
    arsId varchar(10),
    primary key(routeId, routeOrder, stationId, arsId),
    index sbdidx (routeId, routeOrder, stationId, arsId)
)charset=utf8;



-- 서울 버스 노선ID 및 노선순서, 정류장ars에 해당하는 주말,공휴일 / 평일 이용객 비율
create table ratioBusStationUser(
    routeId varchar(10),
    routeOrder int,
    stationId varchar(10),
    arsId varchar(10),
    weekDayRideRatio int,
    weekDayAlightRatio int,
    weekendRideRatio int,
    weekendAlightRatio int,
    primary key(routeId, routeOrder,stationId,arsId),
    foreign key(routeId, routeOrder,stationId,arsId) 
        references seoulBusData(routeId, routeOrder, stationId,arsId),
    index ratioidx (routeId,  routeOrder, stationId,arsId)
)charset=utf8;

-- 서울 버스의 월별 시간대별 이용객에 대한 정보를 저장하는 table
create table monthTimeBusUser(
    routeId varchar(10),
    routeOrder int,
    stationId varchar(10),
    arsId varchar(10),
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
    primary key(routeId,  routeOrder, stationId,arsId),
    foreign key(routeId,  routeOrder, stationId,arsId) 
        references seoulBusData(routeId,  routeOrder, stationId,arsId),
    index mtuindex (routeId,   routeOrder, stationId,arsId)
)charset = utf8;


create table dayType(
    ymd date,
    kind varchar(10),
    primary key(ymd)
);
