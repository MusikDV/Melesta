# -*- coding: utf-8 -*-
import csv
import sqlite3

db_file_name = "melesta.db"
visits_log_file_name = "Visits_Log2.csv"
payments_log_file_name = "Payments_Log2.csv"

#функция для формирования insert
def get_insert_string(table_name, values, expected_col_num):

 insert_string = "insert into " + table_name + " values("
 col_num = 0
 
 for value in values:
  if col_num != 0:
   insert_string += ","
  insert_string += "'"+value+"'"
  col_num += 1
 
 while col_num < expected_col_num:
  insert_string += ",''"
  col_num += 1
 insert_string +=")"

# print(insert_string)

 return insert_string

#подключаемся к базе
conn = sqlite3.connect(db_file_name)
db = conn.cursor()

#создаем таблицы
db.execute("drop table if exists visits")
db.execute("drop table if exists payments")
db.execute("create table visits (date date, playerid int, country text, action text, info text)")
db.execute("create table payments (date date, playerid int, package text, price real)")

#парсим visits_log
log_file  = open(visits_log_file_name, "rt")
reader = csv.reader(log_file)

rownum = 0
for row in reader:
 if rownum == 0:
  header = row
 else:
  db.execute(get_insert_string("visits", row, 5))
 rownum += 1

log_file.close()

#парсим payment_log
log_file  = open(payments_log_file_name, "rt")
reader = csv.reader(log_file)

rownum = 0
for row in reader:
 if rownum == 0:
  header = row
 else:
  db.execute(get_insert_string("payments", row, 4))
 rownum += 1

log_file.close()

#db.execute("select * from payments")
#print(db.fetchall())

conn.commit()
conn.close()
  
