import sqlite3
conn = sqlite3.connect("sqlite.db")
cursor = conn.cursor()
print("Connected to SQLite")

qry = f"SELECT * FROM emp_attendance where emp_id = '70299794'"
print("qry :: "+qry)

cursor.execute(qry)
records = cursor.fetchall()
print("Total rows are:  ", len(records))
print("Printing each row")


if records == 0:
    print("No Records")

for n in records:
    print(n[0] +"  "+n[1])