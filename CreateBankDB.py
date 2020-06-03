import sqlite3
conn = sqlite3.connect('BankDB.db')
c = conn.cursor()
c.execute("CREATE TABLE USERS(NAME TEXT, USERNAME TEXT, PASSWORD TEXT, ACCOUNT_ID INTEGER, PubKey TEXT);")
conn.commit()
c.execute("CREATE TABLE SAMPE(ACCOUNT_ID INTEGER, SENDER_ID INTEGER, RECEIVER_ID INTEGER, TRANSACTION_AMOUNT REAL, DOT TEXT, TOT TEXT, TRANSACTION_ID TEXT);")
print("Database created.")
conn.commit()
conn.close()