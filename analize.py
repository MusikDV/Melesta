# -*- coding: utf-8 -*-

import datetime
import csv
import sqlite3

db_file_name = "melesta.db"
out_file_name = "out.csv"

conn = sqlite3.connect(db_file_name)
db = conn.cursor()

db.execute("select distinct playerid from payments")
db.execute("select min(date), playerid from visits")
db.execute("select a.date, a.playerid from visits as a, (select distinct playerid from payments) as b where a.playerid = b.playerid")
db.execute("select date(a.date) as date, a.playerid from visits as a, (select distinct playerid from payments) as b where a.playerid = b.playerid group by a.playerid order by date")
db.execute("select c.date, count(c.date) from (select date(a.date) as date from visits as a, (select distinct playerid from payments) as b where a.playerid = b.playerid group by a.playerid order by date) as c group by c.date")
db.execute("select * from visits where playerid=0 order by date")
#for record in db.fetchall():
# print(record)
db.execute("select * from payments where playerid=0 order by date")
#for record in db.fetchall():
# print(record)
#for row in db:
# print (row)

#db.execute("select date(date), playerid from visits order by date")
#for record in db.fetchall():
# print(record)

#db.execute("select sum(cnt) from (select date, count(playerid) as cnt from (select distinct playerid, date from (select date(date) as date, playerid from visits)) group by date)")
#print(db.fetchone()[0])
#db.execute("select sum(cnt) from (select date, count(playerid) as cnt from (select playerid, date from (select date(date) as date, playerid from visits)) group by date)")
#print(db.fetchone()[0])
#db.execute("select count(*) from visits")
#print(db.fetchone()[0])

#db.execute("select a.date, a.adate, b.bdate, a.playerid from (select date(date) as date, date as adate, playerid from visits) as a, (select date(date) as date, date as bdate, playerid from payments) as b where a.date = b.date and a.playerid = b.playerid")
#for record in db.fetchall():
# print(record)

db.execute("select distinct price from payments")
#for record in db.fetchall():
# print(record)

db.execute("select distinct country from visits")
#for record in db.fetchall():
# print(record)

db.execute("select count(*) from visits where time(date) > '00:00:00' and time(date) < '01:00:00'")
#print(db.fetchone()[0])

db.execute("select avg(cnt) from (select count(action) as cnt, playerid from visits where playerid in (select distinct playerid from payments) and action = 'Level' and info = '1' group by playerid)")
#for record in db.fetchall():
# print(record)

db.execute("select avg(cnt) from (select count(action) as cnt, playerid from visits where playerid not in (select distinct playerid from payments) and action = 'Level' and info = '1' group by playerid)")
#for record in db.fetchall():
# print(record)

db.execute("select distinct playerid, date from visits where date(date) between '2014-01-01' and '2014-01-03' order by date")
#for record in db.fetchall():
# print(record)

db.execute("select distinct playerid, date from visits where (date(date) >= '2014-01-01') and (date(date) < '2014-01-03') order by date")
#for record in db.fetchall():
# print(record)


db.execute("select count(action) as cnt, playerid from visits where playerid in (select distinct playerid from payments) and action = 'Level' and info = '1' group by playerid")
#for record in db.fetchall():
# print(record)

db.execute("select count(action) as cnt, playerid from visits where playerid not in (select distinct playerid from payments) and action = 'Level' and info = '1' group by playerid")
#for record in db.fetchall():
# print(record)


db.execute("select distinct action from visits")
#for record in db.fetchall():
# print(record)

db.execute("select count(*) from payments")
#print(db.fetchone()[0])

db.execute("select min(c.adate), c.bdate, c.playerid from (select a.date as date, a.adate as adate, b.bdate as bdate, a.playerid as playerid from (select date(date) as date, date as adate, playerid from visits) as a, (select date(date) as date, date as bdate, playerid from payments) as b where a.adate > b.bdate and a.playerid = b.playerid) as c group by c.bdate order by playerid")
#for record in db.fetchall():
# print(record)

db.execute("select max(date), playerid from (select min(date) as date, playerid from visits group by playerid)")
#print(db.fetchone()[0])

db.execute("select count(*) from (select distinct playerid from visits where info = '1')")
#print(db.fetchone()[0])

db.execute("select max(cnt), playerid from (select count(*) as cnt, playerid from visits group by playerid)")
#print(db.fetchone())

db.execute("select * from visits where playerid = 1255 order by date")
#for record in db.fetchall():
# print(record)
db.execute("select * from payments where playerid = 1255 order by date")
#for record in db.fetchall():
# print(record)

db.execute("select info from visits where action <> 'Level' and info <> ''")
#for record in db.fetchall():
# print(record)

db.execute("select sum(price), date(date) from payments where date(date) = '2015-02-12'")
#print(db.fetchone())

db.execute("select count(distinct playerid), date(date) from visits where date(date) = '2015-02-12'")
#print(db.fetchone())

db.execute("select sum(price) as a, playerid from payments group by playerid order by a desc")
db.execute("select count(playerid), 10 from (select sum(price) as a, playerid from payments group by playerid order by a desc) where a<10")
print(db.fetchone())
db.execute("select count(playerid), 20 from (select sum(price) as a, playerid from payments group by playerid order by a desc) where a>10 and a<20 ")
print(db.fetchone())
db.execute("select count(playerid), 30 from (select sum(price) as a, playerid from payments group by playerid order by a desc) where a>20 and a<30 ")
print(db.fetchone())
db.execute("select count(playerid), 40 from (select sum(price) as a, playerid from payments group by playerid order by a desc) where a>30 and a<40 ")
print(db.fetchone())
db.execute("select count(playerid), 50 from (select sum(price) as a, playerid from payments group by playerid order by a desc) where a>40 and a<50 ")
print(db.fetchone())
db.execute("select count(playerid), 60 from (select sum(price) as a, playerid from payments group by playerid order by a desc) where a>50 and a<60 ")
print(db.fetchone())
db.execute("select count(playerid), 70 from (select sum(price) as a, playerid from payments group by playerid order by a desc) where a>60 and a<70 ")
print(db.fetchone())
db.execute("select count(playerid), 80 from (select sum(price) as a, playerid from payments group by playerid order by a desc) where a>70 and a<80 ")
print(db.fetchone())
db.execute("select count(playerid), 90 from (select sum(price) as a, playerid from payments group by playerid order by a desc) where a>80 and a<90 ")
print(db.fetchone())
db.execute("select count(playerid), 100 from (select sum(price) as a, playerid from payments group by playerid order by a desc) where a>90 and a<100 ")
print(db.fetchone())
db.execute("select count(playerid) from (select sum(price) as a, playerid from payments group by playerid order by a desc) where a>100 ")
print(db.fetchone())

db.execute("select count(*) from visits")
print(db.fetchone())

print("!!!")

db.execute("select count(*) from (select a.date as ad, a.playerid as ap, date(a.date) as _add from visits as a, visits as b where a.playerid = b.playerid and date(a.date) = date(b.date) and a.date <> b.date order by ap, _add)")
for record in db.fetchall():
 print(record)

db.execute("select count(*)*1.0/count(distinct playerid) from visits where country='China'")
print(db.fetchone())
db.execute("select count(*)*1.0/count(distinct playerid) from visits where country='Germany'")
print(db.fetchone())
db.execute("select count(*)*1.0/count(distinct playerid) from visits where country='Russia'")
print(db.fetchone())
db.execute("select count(*)*1.0/count(distinct playerid) from visits where country='USA'")
print(db.fetchone())

db.execute("select action from visits group by action")
for record in db.fetchall():
 print(record)

#db.execute("select count() select visits.date, playerid, b.a from visits, (select date(date) as a, playerid as p from visits) as b where date(visits.date) = b.a and visits.playerid = b.p")
#for record in db.fetchall():
# print(record)

#db.execute("select t.cnt, visits.date, visits.playerid from visits, (select count(date) as cnt, date(date) as date, playerid from visits group by playerid, date(date)) as t where t.cnt > 1 and t.date = date(visits.date) and t.playerid = visits.playerid order by t.playerid, visits.date")
#for record in db.fetchall():
# print(record)

#db.execute("select distinct package, price from payments")
#for record in db.fetchall():
# print(record)

db.execute("select count(*) from payments")
#print(db.fetchone())

db.execute("select c.adate, c.bdate, c.playerid from (select a.date as date, a.adate as adate, b.bdate as bdate, a.playerid as playerid from (select date(date) as date, date as adate, playerid from visits) as a, (select date(date) as date, date as bdate, playerid from payments) as b where a.adate > b.bdate and a.playerid = b.playerid) as c order by c.bdate, playerid, c.adate")
#for record in db.fetchall():
# print(record)

db.execute("select max(date) from (select min(date) as date from visits group by playerid)") 
for record in db.fetchall():
 print(record)

out_file = open(out_file_name,"wt")
writer = csv.writer(out_file)
writer.writerows(db)

db.execute("select p.pd, v.vd, p.pp from (select min(date) as pd, playerid as pp from payments group by playerid) as p, (select min(date) as vd, playerid as vp from visits group by playerid) as v where v.vp = p.pp order by p.pp")
for record in db.fetchall():
 print(record)
db.execute("select p.pd, v.vd, p.pp from (select min(date) as pd, playerid as pp from payments group by playerid) as p, (select min(date) as vd, playerid as vp from visits group by playerid) as v where v.vp = p.pp order by p.pp")
cnt = 0
cnt2 = 0
cnt3 = 0
late = datetime.timedelta(days = 1000)
t_b_p = datetime.timedelta()
for record in db.fetchall():
 pay_date =  datetime.datetime.strptime(record[0], "%Y-%m-%d %H:%M:%S.%f")
 act_date = datetime.datetime.strptime(record[1], "%Y-%m-%d %H:%M:%S.%f")
 diff = pay_date - act_date
 t_b_p += diff
 cnt += 1
 if diff < late:
  late = diff
  print(record[2])
 if diff < datetime.timedelta():
  if diff < datetime.timedelta(days = -30):
   cnt3 += 1
   print(diff)
  cnt2 += 1
t_b_p /= cnt
print("t_b_p", t_b_p, late, cnt2, cnt3)

db.execute("select count(info) as cnt, max(info) as mx, playerid from visits where action = 'Level' and info <> '10' and info <> '11' and info <> '12' group by playerid")
for record in db.fetchall():
 if record[0] < int(record[1]):
  print("!!!!!!!!",record)

out_file.close()