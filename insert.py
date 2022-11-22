import sqlite3
conn = sqlite3.connect("sqlite.db")

ins = '''
    insert into emp_attendance (emp_id,emp_name,attend_date,attend_time) values 
        ('70299794','Rajat','16-04-2022','22:24')
'''
conn.execute(ins)
conn.commit()
conn.close()
