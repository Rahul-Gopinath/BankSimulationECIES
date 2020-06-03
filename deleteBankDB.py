import sqlite3
conn = sqlite3.connect('BankDB.db')
c = conn.cursor()
c.execute("DROP TABLE USERS")
conn.commit()
c.execute("DROP TABLE SAMPE")
conn.commit()
conn.close()