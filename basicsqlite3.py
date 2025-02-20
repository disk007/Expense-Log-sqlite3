
import sqlite3

conn=sqlite3.connect('expense.sqlite3')
c=conn.cursor()#สร้างตัวดำเนินการ (อยากได้อะไรใช้ตัวนี้)

c.execute("""CREATE TABLE IF NOT EXISTS expenselist (
				ID INTEGER PRIMARY KEY AUTOINCREMENT,
				transactionid TEXT,
				datetime TEXT,
				title TEXT,
				expense INTEGER,
				amount INTEGER,
				total INTEGER

			)""")

def insert_expense(transactionid,datetime,title,expense,amount,total):
	ID=None
	with conn:
		c.execute("""INSERT INTO expenselist VALUES (?,?,?,?,?,?,?)""",
			(ID,transactionid,datetime,title,expense,amount,total))
	conn.commit()#บันทึกข้อมูลงในฐานข้อมูล
	print("Inser Success")

def show_expense():
	with conn:
		c.execute("SELECT * FROM expenselist")
		expense=c.fetchall()#คำสั่งให้ดึงข้อมูลออกมา
		print(expense)
	return expense

def update_expense(transactionid,title,expense,amount,total):
	with conn:
		c.execute("""UPDATE expenselist SET title=?,expense=?,amount=?,total=? WHERE transactionid=?""",
			([title,expense,amount,total,transactionid]))
	conn.commit()
	print("Data update")

def delete_expense(transactionid):
	with conn:
		c.execute("DELETE FROM expenselist WHERE transactionid=?",([transactionid]))
	conn.commit()
	print("Data Delete")

#delete_expense('20212093949')
show_expense()

#insert_expense('20212093949','วันเสาร์-2021-07-12','ข้าวเหนียว',50,2,100)
	
print("success")