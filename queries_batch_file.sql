select count(*) from Report where year(date) = 2000;
select ID, r.City, State, Date, Time, Shape, Summary, Duration, Posted from Report r inner join Location l on r.city = l.city where l.state = "PA";
select ID, r.City, State, Date, Time, Shape, Summary, Duration, Posted from Report r inner join Location l on r.city = l.city where shape = "Triangle";
select ID, r.City, State, Date, Time, Shape, Summary, Duration, Posted from Report r inner join Location l on r.city = l.city where duration >= "24:00:00";
select ID, r.City, State, Date, Time, Shape, Summary, Duration, Posted from report r inner join location l on r.city = l.city where year(posted) = 2021;
select date from report r inner join location l on r.city = l.city where date is not null order by date limit 1;
select count(*) from report;
select ID, r.City, State, Date, Time, Shape, Summary, Duration, Posted from report r inner join location l on r.city = l.city where shape = "circle" and l.state = "AZ" and year(date) < 2003;
select summary from report r inner join location l on r.city = l.city where l.state is null;