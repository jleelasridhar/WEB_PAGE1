from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Fake in-memory database (Vercel safe)
users = {
    1: {"username": "admin", "password": "admin123", "role": "admin"},
    2: {"username": "user1", "password": "user123", "role": "user"},
    3: {"username": "user2", "password": "user123", "role": "user"}
}

user_details = {
    1: {
        "name": "Admin Kumar",
        "age": 35,
        "dob": "1989-05-10",
        "phone": "9876543210",
        "email": "admin@bank.com",
        "aadhar": "123456789012",
        "account": "111122223333"
    },
    2: {
        "name": "Rahul",
        "age": 22,
        "dob": "2002-03-12",
        "phone": "9123456780",
        "email": "rahul@gmail.com",
        "aadhar": "234567890123",
        "account": "222233334444"
    },
    3: {
        "name": "Priya",
        "age": 23,
        "dob": "2001-07-20",
        "phone": "9234567810",
        "email": "priya@gmail.com",
        "aadhar": "345678901234",
        "account": "333344445555"
    }
}


@app.route("/")
def login_page():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    username_input = request.form['username']
    password_input = request.form['password']

    # ❌ Vulnerability 1: Plain text password check
    # ❌ Vulnerability 2: No session handling
    # ❌ Vulnerability 3: No account lock / brute force protection

    for user_id, user in users.items():
        if user["username"] == username_input and user["password"] == password_input:
            return redirect(f"/dashboard/{user_id}")

    return "Invalid Login"


@app.route("/dashboard/<int:user_id>")
def dashboard(user_id):

    # ❌ Vulnerability 4: Broken Access Control
    # Anyone can change URL and view any user data

    if user_id not in users:
        return "User Not Found"

    user = users[user_id]
    details = user_details[user_id]

    return render_template(
        "dashboard.html",
        user=user["username"],     # ❌ XSS possible if injected
        role=user["role"],
        details=details
    )


if __name__ == "__main__":
    app.run(debug=True)
