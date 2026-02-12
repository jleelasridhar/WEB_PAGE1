from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "weaksecret"   # A04 Weak crypto


# SQLite connection
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


# A01: Broken Access Control
@app.route("/dashboard/<int:user_id>")
def dashboard(user_id):

    conn = get_db()
    cursor = conn.cursor()

    # ❌ No session validation (IDOR)
    cursor.execute(f"SELECT * FROM users WHERE id={user_id}")
    user = cursor.fetchone()

    if not user:
        return "User not found"

    cursor.execute(f"SELECT * FROM user_details WHERE user_id={user_id}")
    details = cursor.fetchone()

    conn.close()

    return render_template(
        "dashboard.html",
        user=user['username'],  # XSS vulnerable
        details=details
    )


# A02 Security Misconfiguration
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
