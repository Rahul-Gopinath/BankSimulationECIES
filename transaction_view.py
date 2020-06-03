import sqlite3
import sys

conn = sqlite3.connect('BankDB.db')
c = conn.cursor()

def trans():
    for i in c.execute("SELECT * FROM sampe WHERE ACCOUNT_ID!=1;"):
        print(i)

def users():
    for i in c.execute("SELECT * FROM USERS;"):
        print(i)


while True:
    ptr = int(input("1. Users\n2. Transactions\n3. Exit\n"))
    if ptr == 1:
        users()
    elif ptr == 2:
        trans()
    elif ptr == 3:
        sys.exit()
    else:
        print("Wrong input\n")
