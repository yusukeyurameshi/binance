#!/usr/bin/python3

import cx_Oracle

conn = cx_Oracle.connect()
cursor = conn.cursor()
cursor.execute("alter session set nls_date_format='mm/dd/yyyy hh24:mi:ss'")

cursor.execute("select sysdate from dual")

rows = cursor.fetchall()

for row in rows:

    print(row[0])


cursor.close()
conn.close()


