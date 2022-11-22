import sqlite3
conn = sqlite3.connect("sqlite.db")
conn.execute(''' 
        create table emp_attendance(
            emp_id VARCHAR(50),
            emp_name VARCHAR(50),
            attend_date VARCHAR(20),
            attend_time VARCHAR(10)
        )
    ''')
conn.close()