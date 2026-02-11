from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# MySQL connection
"""db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="vulnerable_app"
)

cursor = db.cursor()"""

@app.route("/")
def login_page():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    username_input = request.form['username']
    password_input = request.form['password']

    # Temporary login without database (for Render deployment)

    if username_input == "admin" and password_input == "admin123":
        return "Login Success"
    else:
        return "Invalid Login"


    if row:
        # row = (id, username, password, role)
        username = row[1]
        user_id = row[0]

        
        details = {
            "name": username,
            "age": 28,
            "dob": "1997-05-12",
            "phone": "9876543210",
            "email": username + "@example.com",
            "aadhar": "1234-5678-9012",
            "account": "AC987654321"
        }

        return render_template(
            "dashboard.html",
            user=username,     # XSS vulnerable
            details=details
        )

    else:
        return "Invalid Login"


if __name__ == "__main__":
    app.run(debug=True)
@app.route("/dashboard/<int:user_id>")
def dashboard_by_id(user_id):

    # ❌ NO AUTH CHECK (Broken Access Control)
    cursor.execute(f"SELECT * FROM users WHERE id={user_id}")
    user = cursor.fetchone()

    if not user:
        return "User not found"

    username = user[1]
    role = user[3]

    cursor.execute(f"SELECT * FROM user_details WHERE user_id={user_id}")
    details_row = cursor.fetchone()

    details = {
        "name": details_row[1],
        "age": details_row[2],
        "dob": details_row[3],
        "phone": details_row[4],
        "aadhar": details_row[5],
        "account": details_row[6],
        "email": details_row[7]
    }

    return render_template(
        "dashboard.html",
        user=username,
        role=role,
        details=details
    )

