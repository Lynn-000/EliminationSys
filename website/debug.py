import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
cnxn = sqlite3.connect("ElimSys.db")
cur = cnxn.cursor()
un = ('Kzyro',)
cur.execute('''SELECT * FROM Administrator WHERE Username = ?''', un)
print(cur.fetchall())