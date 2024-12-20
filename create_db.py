import sqlite3
def create_db():
    con=sqlite3.connect(database=r'tbs.db')
    cur=con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS employee(eid INTEGER PRIMARY KEY AUTOINCREMENT,name text,email text,contact text,pass text,utype text)")
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS services(id INTEGER PRIMARY KEY AUTOINCREMENT,name text,price number,estimated_time text)")
    con.commit()
    
    cur.execute("CREATE TABLE IF NOT EXISTS stock(pid INTEGER PRIMARY KEY AUTOINCREMENT,Supplier text,itemname text,hsncode text,price text,qty text,discount text)")
    con.commit()


create_db()