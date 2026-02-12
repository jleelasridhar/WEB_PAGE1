from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "weaksecret"   # A04 Weak crypto


# -------------------------------
# 🔥 AUTO DATABASE INITIALIZATION
# -------------------------------
def init_db():
    conn = sqlite3.connect("vuln.db")
    cursor = conn.cursor()

    # Create users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT,
        role TEXT
    )
    """)

    # Create user_details table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_details (
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

    # Insert default data if empty
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO users VALUES (1,'admin','admin123','admin')")
        cursor.execute("INSERT INTO users VALUES (2,'user1','password1','user')")

        cursor.execute("""
        INSERT INTO user_details 
        VALUES (1,1,'Admin Kumar',35,'1989-05-10','9876543210',
                'admin@bank.com','123456789012','111122223333')
        """)

        cursor.execute("""
        INSERT INTO user_details 
        VALUES (2,2,'Rahul',22,'2002-03-12','9123456780',
                'rahul@gmail.com','234567890123','222233334444')
        """)

    conn.commit()
    conn.close()


# 🔥 IMPORTANT: Call DB initializer when app loads
init_db()


# -------------------------------
# SQLite connection
# -------------------------------
def get_db():
    conn = sqlite3.connect("vuln.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def login_page():
    return render_template("login.html")


# A05: SQL Injection
@app.route("/login", methods=["POST"])
def login():
    username = request.form['username']
    password = request.form['password']

    conn = get_db()
    cursor = conn.cursor()

    # ❌ SQL Injection vulnerability
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    cursor.execute(query)
    user = cursor.fetchone()

    conn.close()

    if user:
        return redirect(f"/dashboard/{user['id']}")
    else:
        return "Invalid Login"


# A01: Broken Access Control (IDOR)
@app.route("/dashboard/<int:user_id>")
def dashboard(user_id):

    conn = get_db()
    cursor = conn.cursor()

    # ❌ No authentication check
    cursor.execute(f"SELECT * FROM users WHERE id={user_id}")
    user = cursor.fetchone()

    if not user:
        return "User not found"

    cursor.execute(f"SELECT * FROM user_details WHERE user_id={user_id}")
    details = cursor.fetchone()

    conn.close()

    return render_template(
        "dashboard.html",
        user=user['username'],  # XSS vulnerable if template uses |safe
        details=details
    )


# A02 Security Misconfiguration (debug enabled)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
