import sqlite3
conn=sqlite3.connect("orbitlife.db")
cur=conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY,name TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS expenses(user_id INTEGER,amount REAL,category TEXT)")
conn.commit()
def add_user(uid,name):
 cur.execute("INSERT OR IGNORE INTO users VALUES(?,?)",(uid,name)); conn.commit()
def add_expense(uid,amt,cat):
 cur.execute("INSERT INTO expenses VALUES(?,?,?)",(uid,amt,cat)); conn.commit()
def get_expenses(uid):
 cur.execute("SELECT amount,category FROM expenses WHERE user_id=?",(uid,)); return cur.fetchall()
