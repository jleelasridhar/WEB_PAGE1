import sqlite3

conn = sqlite3.connect("vuln.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT,
    role TEXT
)
""")

cursor.execute("""
CREATE TABLE user_details (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    name TEXT,
    age INTEGER,
    dob TEXT,
    phone TEXT,
    email TEXT,
    aadhar TEXT,
    account TEXT
)
""")

cursor.execute("INSERT INTO users VALUES (1,'admin','admin123','admin')")
cursor.execute("INSERT INTO users VALUES (2,'user1','password1','user')")

cursor.execute("INSERT INTO user_details VALUES (1,1,'Admin Kumar',35,'1989-05-10','9876543210','admin@bank.com','123456789012','111122223333')")
cursor.execute("INSERT INTO user_details VALUES (2,2,'Rahul',22,'2002-03-12','9123456780','rahul@gmail.com','234567890123','222233334444')")

conn.commit()
conn.close()

print("Database created successfully")
