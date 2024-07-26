import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
cnxn = sqlite3.connect("../instance/ElimSys.db")
cur = cnxn.cursor()
Username = str(input("Welcome! You can add an administrator account with this process. \n Please enter the username of the administrator account you wish to create: \n"))
Password = str(input("Please enter the password: \n"))
Password2 = str(input("Please confirm the password: \n"))
while Password != Password2: 
    Password2 = str(input("Password does not match! Please confirm your password again: \n"))
Password = generate_password_hash(Password, method = 'pbkdf2:sha256')
f = '''INSERT INTO Administrators(Username, Password) VALUES(?,?)'''
Ph = (Username, Password)
cur.execute(f, Ph)
cur.execute('''SELECT * FROM Administrators''')
print(cur.fetchall())
cnxn.commit()