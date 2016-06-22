# -*- coding: utf-8 -*-

import sqlite3
import datetime

db_file_name = "melesta.db"
day = datetime.timedelta(days=0)
week = datetime.timedelta(weeks=1)
month = datetime.timedelta(weeks=4)

def count_metrics_for_country(country):
 print("Metrics for ", country)
 db.execute("select sum(price) from payments where playerid in (select distinct playerid from visits where country = '" + country + "')")
 c_sum = db.fetchone()[0]
 db.execute("select count(*) from (select distinct playerid from visits where country = '" + country + "')")
 c_pl =  db.fetchone()[0]
 db.execute("select count(*) from (select distinct playerid from visits where country = '" + country + "' and playerid in (select distinct playerid from payments))")
 c_pu =  db.fetchone()[0]
 print(c_pl, c_sum, c_pu, c_pu/c_pl*100, c_sum/c_pl)

def analize_payments(country):
 print("Payments in ", country)
 res = list()
 db.execute("select count(*) from payments where package = 'Package1' and playerid in (select distinct playerid from visits where country = '" + country + "')")
 res.append(db.fetchone()[0])
 db.execute("select count(*) from payments where package = 'Package2' and playerid in (select distinct playerid from visits where country = '" + country + "')")
 res.append(db.fetchone()[0])
 db.execute("select count(*) from payments where package = 'Package3' and playerid in (select distinct playerid from visits where country = '" + country + "')")
 res.append(db.fetchone()[0])
 db.execute("select count(*) from payments where package = 'Package4' and playerid in (select distinct playerid from visits where country = '" + country + "')")
 res.append(db.fetchone()[0])
 db.execute("select count(*) from payments where package = 'Package5' and playerid in (select distinct playerid from visits where country = '" + country + "')")
 res.append(db.fetchone()[0])
 db.execute("select count(*) from payments where package = 'Package6' and playerid in (select distinct playerid from visits where country = '" + country + "')")
 res.append(db.fetchone()[0])
 print(res)

conn = sqlite3.connect(db_file_name)
db = conn.cursor()

#определяем количество активных учетных записей

db.execute("select count(*) from (select distinct playerid from visits)")
acc_count = db.fetchone()[0]
print("Total users: ", acc_count)

#определяем количество платящих пользователей

db.execute("select count(*) from (select distinct playerid from payments)")
pay_acc_count = db.fetchone()[0]
print("Paying users:", pay_acc_count)

#процент платящих PU

pu=pay_acc_count/acc_count*100
print("PU: ", pu)

#LTV

db.execute("select sum(price) from payments")
sum = float(db.fetchone()[0])
print("Total payed: ",sum)
print("LTV", sum/acc_count)

#рассчет метрик по странам

count_metrics_for_country("Germany")
count_metrics_for_country("USA")
count_metrics_for_country("China")
count_metrics_for_country("Russia")

analize_payments("Germany")
analize_payments("USA")
analize_payments("China")
analize_payments("Russia")

#время жизни учетной записи LT

db.execute("select min(date), max(date), playerid from visits group by playerid")
lt = datetime.timedelta()
con_d = 0
con_w = 0
con_m = 0
min_life = datetime.timedelta(days = 800)
max_life = datetime.timedelta(days = 0)
for record in db.fetchall():
 first_visit = datetime.datetime.strptime(record[0],"%Y-%m-%d %H:%M:%S.%f")
 last_visit = datetime.datetime.strptime(record[1],"%Y-%m-%d %H:%M:%S.%f")
 life = last_visit - first_visit
 if life < min_life:
  min_life = life
 if life > max_life:
  max_life = life
  pl = record[2]
 #print(life)
 lt += (life/acc_count)
 if life > day:
  con_d += 1
  if life > week:
   con_w += 1
   if life > month:
    con_m +=1

print("lifetime", min_life, max_life, pl, lt, con_d/acc_count, con_w/acc_count, con_m/acc_count)

#среднее количество сессий на пользователя

db.execute("select count(*) from visits")
aspu = float(db.fetchone()[0])/acc_count
#print(aspu)
db.execute("select min(cnt), max(cnt) from (select count(*) as cnt from visits group by playerid)")
#print(db.fetchone())

#проходимость уравней

db.execute("select a.al, b.pay, b.pay*1.0/a.al, a.info from (select count(distinct playerid) as al, info from visits where action = 'Level' group by info order by info) as a, (select count(distinct playerid) as pay, info from visits where action = 'Level' and playerid in (select distinct playerid from payments) group by info order by info) as b where a.info = b.info")
for record in db.fetchall():
 print(record)

#DAU

db.execute("select date, count(playerid) from (select distinct playerid, date from (select date(date) as date, playerid from visits)) group by date")
with open('graph/dau.js','w') as dau_file:
 print('DAU="DATE,DAU\\n"',file=dau_file)
 for record in db.fetchall():
  print('+"' + record[0].replace('-',''), str(record[1])+'\\n"',file=dau_file,sep=',')

#MAU

this_month = datetime.date(2014,1,1)
next_month = datetime.date(2014,2,1)
last_month = datetime.date(2016,1,1)
with open('graph/mau.js','w') as mau_file:
 print('MAU="DATE,MAU\\n"', file = mau_file)
 while this_month < last_month:
  db.execute("select count(*) from (select distinct playerid from visits where (date(date) >= '" + this_month.strftime("%Y-%m-%d") + "') and (date(date) < '" + next_month.strftime("%Y-%m-%d") +"'))")
  print('+"' + this_month.strftime("%Y%m%d"), str(db.fetchone()[0]) + '\\n"', file = mau_file, sep = ',')
  this_month = next_month
  if this_month.month == 12:
   next_month = next_month.replace(year = this_month.year+1, month = 1)
  else:
   next_month = next_month.replace(month = this_month.month+1)

#время в которое играют в нашу игру

graph = dict()
tmp = list()

db.execute("select date, time(date) as time from visits where country = 'China' and action = 'Level' order by time")
for record in db.fetchall():
 r_time = datetime.datetime.strptime(record[0], "%Y-%m-%d %H:%M:%S.%f").strftime("%H")
 if r_time not in tmp:
  tmp.append(r_time)
 if r_time in graph:
  graph[r_time] += 1
 else:
  graph[r_time] = 1
with open('graph/play_time.js','w') as play_time_file:
 print('PLAY_TIME="TIME,AU\\n"',file=play_time_file)
 for time in tmp:
  print('+"2014/01/01 ' + time + ':00', str(graph[time])+'\\n"',file=play_time_file,sep=',')

#ARPDAU

db.execute("select dau.daudate, rev.summ/dau.cnt from (select count(distinct playerid) as cnt, date(date) as daudate from visits group by date(date)) as dau, (select sum(price) as summ, date(date) as rdate from payments group by date(date)) as rev where dau.daudate = rev.rdate")
with open('graph/arpdau.js','w') as arpdau_file:
 print('ARPDAU="DATE,ARPDAU\\n"',file=arpdau_file)
 for record in db.fetchall():
  print('+"' + record[0].replace('-',''), str(record[1])+'\\n"',file=arpdau_file,sep=',')

#количество платежей, которые были совершены игроком в тот же день когда он был активен

db.execute("select count(*) from (select a.date, a.adate, b.bdate, a.playerid from (select date(date) as date, date as adate, playerid from visits) as a, (select date(date) as date, date as bdate, playerid from payments) as b where a.date = b.date and a.playerid = b.playerid)")
print("Payments in the day player was active: ", db.fetchone()[0])

#среднее количество различных месяцов в которые играл игрок

pid_dict = dict()

db.execute("select date(date), playerid from visits")
for record in db.fetchall():
 pid = record[1]
 date = datetime.datetime.strptime(record[0],"%Y-%m-%d").strftime("%Y%m")
 if pid in pid_dict:
  if date not in pid_dict[pid]:
   pid_dict[pid].append(date)
 else:
  pid_dict[pid] = [date]

avg_month = 0.0
for pid in pid_dict:
 avg_month += len(pid_dict[pid]) / 3000
print("AVG MONTH: ",avg_month)

#среднее время между платежом и следующей активностью игрока

t_diff = []

db.execute("select min(c.adate), c.bdate, c.playerid from (select a.date as date, a.adate as adate, b.bdate as bdate, a.playerid as playerid from (select date(date) as date, date as adate, playerid from visits) as a, (select date(date) as date, date as bdate, playerid from payments) as b where a.adate > b.bdate and a.playerid = b.playerid) as c group by c.bdate order by playerid")
cnt = 0
avg_time_between_pay_and_activity = datetime.timedelta()
for record in db.fetchall():
 pay_date =  datetime.datetime.strptime(record[1], "%Y-%m-%d %H:%M:%S.%f")
 next_activity_date = datetime.datetime.strptime(record[0], "%Y-%m-%d %H:%M:%S.%f")
 t_diff.append(next_activity_date - pay_date)
 avg_time_between_pay_and_activity += next_activity_date - pay_date
 cnt += 1
avg_time_between_pay_and_activity /= cnt
print("Pay Act", avg_time_between_pay_and_activity)

day_7 = datetime.timedelta(days = 7)
cnt_7 = 0
day_14 = datetime.timedelta(days = 14)
cnt_14 = 0
day_21 = datetime.timedelta(days = 21)
cnt_21 = 0
day_28 = datetime.timedelta(days = 28)
cnt_28 = 0
cnt_b = 0

for diff in t_diff:
 if diff > day_28:
  cnt_b += 1
 if diff > day_21 and diff < day_28:
  cnt_28 +=1
 if diff > day_14 and diff < day_21:
  cnt_21 +=1
 if diff > day_7 and diff < day_14:
  cnt_14 +=1
 if diff < day_7:
  cnt_7 += 1
print(cnt_7,cnt_14,cnt_21,cnt_28,cnt_b)

db.execute("select max(c.adate), c.bdate, c.playerid from (select a.date as date, a.adate as adate, b.bdate as bdate, a.playerid as playerid from (select date(date) as date, date as adate, playerid from visits) as a, (select date(date) as date, date as bdate, playerid from payments) as b where a.adate < b.bdate and a.playerid = b.playerid) as c group by c.bdate order by playerid")
cnt = 0
avg_time_between_pay_and_activity = datetime.timedelta()
for record in db.fetchall():
 pay_date =  datetime.datetime.strptime(record[1], "%Y-%m-%d %H:%M:%S.%f")
 next_activity_date = datetime.datetime.strptime(record[0], "%Y-%m-%d %H:%M:%S.%f")
 avg_time_between_pay_and_activity += pay_date - next_activity_date
 cnt += 1
avg_time_between_pay_and_activity /= cnt
print("Act Pay", avg_time_between_pay_and_activity)

# среднее количество действий Buy

db.execute("select count(*) from visits where action = 'Buy' and playerid in (select distinct playerid from payments)")
buy_pay = db.fetchone()[0]
db.execute("select count(*) from visits where action = 'Buy' and playerid not in (select distinct playerid from payments)")
buy_free = db.fetchone()[0]
print(buy_pay*1.0/pay_acc_count, buy_free*1.0/(acc_count-pay_acc_count))
 
conn.close()