import sys
#from PyQt5 import QtGui
#from PyQt5 import QtCore
from PyQt5 import QtWidgets
import sqlite3
import hashlib
import seccure as s
import datetime

class Window(QtWidgets.QMainWindow):
    
    def __init__(self):
        super(Window, self).__init__()
        self.setWindowTitle("Bank Simulation")
        self.resize(400, 300)
        self.move(700, 400)
        self.Controls()
        self.show()
 
    def Controls(self):
        self.UserName = QtWidgets.QLineEdit(self)
        self.Password = QtWidgets.QLineEdit(self)
        self.Password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.UserName.move(180, 100)
        self.Password.move(180, 150)
        self.TextUser = QtWidgets.QLabel("UserName: ", self)
        self.TextPass = QtWidgets.QLabel("Password: ", self)
        self.TextUser.move(100, 100)
        self.TextPass.move(100, 150)
        self.ExitButton = QtWidgets.QPushButton("Exit", self)
        self.ExitButton.move(150, 250)
        self.ExitButton.clicked.connect(self.on_click_exit)
        self.LoginButton = QtWidgets.QPushButton("Login", self)
        self.LoginButton.move(200, 200)
        self.LoginButton.clicked.connect(self.on_click_login)
        self.SignUpButton = QtWidgets.QPushButton("Sign Up", self)
        self.SignUpButton.move(100, 200)
        self.SignUpButton.clicked.connect(self.on_click_signup)
        
    def on_click_signup(self):
        self.SignUp = SignUpWindow()
 
    def on_click_exit(self):
        sys.exit()
    
    def on_click_login(self):
        self.conn = sqlite3.connect("BankDB.db")
        self.c = self.conn.cursor()
        self.h = hashlib.sha512()
        self.h.update(self.Password.text().encode())
        self.hash = self.h.digest()
        for i in self.c.execute("SELECT * FROM USERS;"):
            if i[1] == self.UserName.text() and i[2] == self.hash:
                self.Login = LoginedScreen(i[3])
                self.close()

class LoginedScreen(QtWidgets.QMainWindow):
    
    def __init__(self, accID):
        super(LoginedScreen, self).__init__()
        self.accID = accID
        self.resize(400, 400)
        self.move(600, 250)
        self.setWindowTitle("Welcome {}".format('USER'))
        self.ButtonTL = QtWidgets.QPushButton("Transaction Log", self)
        self.ButtonTL.clicked.connect(self.on_click_TL)
        self.ButtonTL.resize(self.ButtonTL.sizeHint())
        self.ButtonTF = QtWidgets.QPushButton("Transfer Funds", self)
        self.ButtonTF.move(100, 300)
        self.ButtonTL.move(100, 200)
        self.ButtonTF.resize(self.ButtonTF.sizeHint())
        self.ButtonTF.clicked.connect(self.on_click_TF)
        self.ButtonExit = QtWidgets.QPushButton("Log Out", self)
        self.ButtonExit.resize(self.ButtonExit.sizeHint())
        self.ButtonExit.move(100, 350)
        self.ButtonExit.clicked.connect(self.on_click_exit)
        self.TotalBalance = QtWidgets.QPushButton("Net Balance", self)
        self.TotalBalance.resize(self.TotalBalance.sizeHint())
        self.TotalBalance.move(100, 150)
        self.TotalBalance.clicked.connect(self.on_click_net_balance)
        self.show()
 
    def on_click_net_balance(self):
        self.NetBalanceScreen = NetBalanceScreen(self.accID)
 
    def on_click_exit(self):
        sys.exit()
 
    def on_click_TF(self):
        self.TF = TransferFundsWindow(self.accID)
 
    def on_click_TL(self):
        self.TL = Transaction_log(self.accID)

    def hashTransaction(time, accID):
        hash = hashlib.sha512()
        time = str(time).split(':')
        time = ''.join(time) + str(accID)
        hash.update(time.encode())
        return hash.digest()

class TransferFundsWindow(QtWidgets.QMainWindow):
    
    def __init__(self, accID):
        super(TransferFundsWindow, self).__init__()
        self.resize(400, 400)
        self.accID = accID
        self.move(700, 400)
        self.LabelSendTo = QtWidgets.QLabel("Send To:", self)
        self.LabelAmount = QtWidgets.QLabel("Amount:", self)
        self.LabelSendTo.move(145, 100)
        self.LabelAmount.move(145, 200)
        self.ReceiversID = QtWidgets.QLineEdit(self)
        self.Amount = QtWidgets.QLineEdit(self)
        self.ReceiversID.move(200, 100)
        self.Amount.move(200, 200)
        self.ButtonSend = QtWidgets.QPushButton("Send", self)
        self.BUttonCancel = QtWidgets.QPushButton("Cancel", self)
        self.ButtonSend.move(100, 300)
        self.BUttonCancel.move(200, 300)
        self.BUttonCancel.clicked.connect(self.on_click_cancel)
        self.ButtonSend.clicked.connect(self.on_click_send)
        self.show()
 
    def on_click_send(self):
        self.conn = sqlite3.connect('BankDB.db')
        self.c = self.conn.cursor()
        self.date = datetime.datetime.now()
        self.id = s.encrypt(self.hashTransaction(self.date.time(), self.accID).encode(),str(s.passphrase_to_pubkey(b'my private key')))
        self.amt = s.encrypt(self.Amount.text().encode(),str(s.passphrase_to_pubkey(b'my private key')))
        print("Transaction ID : " + str(self.id))
        print("\nAmount sent : " + str(self.amt))
        self.c.execute('INSERT INTO SAMPE VALUES(?, ?, ?, ?, ?, ?, ?);', [(self.accID),(self.accID), (self.ReceiversID.text()), self.amt , (str(self.date.time())), (str(self.date.date())), self.id])
        print("\nSuccessfully Transferred")
        # self.fetchdata = self.c.execute('SELECT NETBALANCE FROM USERS where ACCOUNT_ID = ?', [(self.accID)])
        # for i in self.fetchdata:
        # self.intbalnow = i[0]
        # self.c.execute('UPDATE USERS SET NETBALANCE = ? WHERE ACCOUNT_ID =?',[(self.intbalnow - int(self.Amount.text())), (self.accID)])
        self.conn.commit()
        self.close()
        
    def hashTransaction(self, time, accID):
        hash = hashlib.sha512()
        time = str(time).split(':')
        time = ''.join(time) + str(accID)
        hash.update(time.encode())
        return str(hash.digest())
        
    def on_click_cancel(self):
        self.close()

class Transaction_log(QtWidgets.QTableWidget):
 
    def __init__(self, accID):
        super(Transaction_log, self).__init__()
        self.accID = accID
        self.setWindowTitle("Welcome User")
        self.resize(1200, 600)
        self.tableItem = QtWidgets.QTableWidgetItem()
        self.setRowCount(10)
        self.setColumnCount(6)
        self.setHorizontalHeaderLabels(('Sender', 'Receiver', 'Transaction Amount','Time of Transaction', 'Date of Transaction', 'Transaction ID'))
        self.setColumnWidth(0, 200)
        self.setColumnWidth(1, 200)
        self.setColumnWidth(2, 200)
        self.setColumnWidth(3, 200)
        self.setColumnWidth(4, 200)
        self.setColumnWidth(5, 200)
        self.fetch()
        self.show()
 
    def fetch(self):
        self.conn = sqlite3.connect('BankDB.db')
        self.c = self.conn.cursor()
        self.data = self.c.execute('SELECT SENDER_ID, RECEIVER_ID, TRANSACTION_AMOUNT, DOT, TOT, TRANSACTION_ID from SAMPE where ACCOUNT_ID = ? or RECEIVER_ID = ?;', [(self.accID), (self.accID)])
        j = 0
        for i in self.data:
            self.setItem(j, 0, QtWidgets.QTableWidgetItem(str(i[0])))
            self.setItem(j, 1, QtWidgets.QTableWidgetItem(str(i[1])))
            self.setItem(j, 2, QtWidgets.QTableWidgetItem(str(s.decrypt(i[2],b'my private key'))))
            self.setItem(j, 3, QtWidgets.QTableWidgetItem(str(i[3])))
            self.setItem(j, 4, QtWidgets.QTableWidgetItem(str(i[4])))
            self.setItem(j, 5, QtWidgets.QTableWidgetItem(str(i[5])))
            j += 1
            
class SignUpWindow(QtWidgets.QMainWindow):
    
    def __init__(self):
        super(SignUpWindow, self).__init__()
        self.setWindowTitle("Sign Up Window")
        self.resize(500, 500)
        self.Control()
        self.show()
 
    def Control(self):
        self.TextName = QtWidgets.QLabel("Name:", self)
        self.TextName.move(200, 50)
        self.TextUserName = QtWidgets.QLabel("User Name:", self)
        self.TextUserName.move(170, 100)
        self.TextPassword = QtWidgets.QLabel("Password:", self)
        self.TextPassword.move(180, 150)
        self.TextAccountNumber = QtWidgets.QLabel("Account Number:", self)
        self.TextAccountNumber.move(130, 200)
        self.TextAccountNumber.resize(self.TextAccountNumber.sizeHint())
        self.TextNetBalance = QtWidgets.QLabel("Net Balance:", self)
        self.TextNetBalance.move(160, 250)
        self.NameField = QtWidgets.QLineEdit(self)
        self.NameField.move(250, 50)
        self.User_NameField = QtWidgets.QLineEdit(self)
        self.User_NameField.move(250, 100)
        self.PasswordField = QtWidgets.QLineEdit(self)
        self.PasswordField.setEchoMode(QtWidgets.QLineEdit.Password)
        self.PasswordField.move(250, 150)
        self.Account_NumberField = QtWidgets.QLineEdit(self)
        self.Account_NumberField.move(250, 200)
        self.NetBalance = QtWidgets.QLineEdit(self)
        self.NetBalance.move(250, 250)
        self.SubmitButton = QtWidgets.QPushButton("Submit", self)
        self.SubmitButton.move(280, 400)
        self.CancelButton = QtWidgets.QPushButton("Cancel", self)
        self.CancelButton.move(180, 400)
        self.SubmitButton.clicked.connect(self.on_click_submit)
        self.CancelButton.clicked.connect(self.on_click_cancel)
        
    def on_click_submit(self):
        self.conn = sqlite3.connect("BankDB.db")
        self.c = self.conn.cursor()
        self.h = hashlib.sha512()
        self.h.update(self.PasswordField.text().encode())
        self.hash = self.h.digest()
        print("The message digest : " + str(self.hash))
        print("The message digest size : " + str(self.h.digest_size))
        self.publicKey = str(s.passphrase_to_pubkey(b'my private key'))
        self.date = datetime.datetime.now()
        self.c.execute("INSERT INTO USERS(NAME, USERNAME, PASSWORD, ACCOUNT_ID, PubKey) VALUES(?, ?, ?, ?, ?);", [(self.NameField.text()),(self.User_NameField.text()), (self.hash), (self.Account_NumberField.text()), (self.publicKey)])
        self.c.execute("INSERT INTO SAMPE VALUES(00001, 00001, ?, ?, ?, ?, ?);",[(self.Account_NumberField.text()), (s.encrypt(self.NetBalance.text().encode(),self.publicKey)), (str(self.date.time())), (str(self.date.date())),self.hash_Transaction(self.date.time(), self.Account_NumberField.text())]);
        self.conn.commit()
        self.conn.close()
        self.close()
        
    def hash_Transaction(self, time, accID):
        hash = hashlib.sha512()
        time = str(time).split(':')
        time = ''.join(time) + str(accID)
        hash.update(time.encode())
        return hash.digest()
 
    def on_click_cancel(self):
        self.result = QtWidgets.QMessageBox.question(self, 'Alert', "Do you want to leave this page ?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if self.result == QtWidgets.QMessageBox.Yes:
            self.close()

class NetBalanceScreen(QtWidgets.QMainWindow):
    
    def __init__(self, accID):
        super(NetBalanceScreen, self).__init__()
        self.resize(200, 200)
        self.accID = accID
        self.CalBAL()
        self.Label = QtWidgets.QLabel("Net Balance", self)
        self.Balance = QtWidgets.QLineEdit(self)
        self.Balance.setText(str(self.NETBAL))
        self.Balance.setReadOnly(True)
        self.Label.move(50, 50)
        self.Balance.move(50, 100)
        self.show()
 
    def CalBAL(self):
        self.conn = sqlite3.connect('BankDB.db')
        self.c = self.conn.cursor()
        self.data = self.c.execute('SELECT TRANSACTION_AMOUNT FROM SAMPE WHERE RECEIVER_ID = ?;', [(self.accID)])
        self.pos = 0
        for i in self.data:
            # self.pos += int(i[0])
            self.pos += float(s.decrypt(i[0], b'my private key').decode())
            # print(s.decrypt(str(i[0]).encode(), b'my private key'))
        self.data = self.c.execute('SELECT TRANSACTION_AMOUNT FROM SAMPE WHERE SENDER_ID = ?;', [(self.accID)])
        self.neg = 0
        for i in self.data:
            pass
            self.neg += float(s.decrypt(i[0], b'my private key').decode())
            #print(s.decrypt(str(i[0]).encode(), b'my private key'))
        # self.bald = self.c.execute('SELECT NETBALANCE FROM USERS WHERE ACCOUNT_ID = ?;',[(self.accID)])
        print(self.accID)
        self.NETBAL = self.pos - self.neg

if __name__ == "__main__":
    App = QtWidgets.QApplication(sys.argv)
    GUI = Window()
    sys.exit(App.exec_())