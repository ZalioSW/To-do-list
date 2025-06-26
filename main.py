from flask import Flask, session, render_template, jsonify, redirect, url_for, request
import sqlite3
import bcrypt

conn = sqlite3.connect('uporabniki.sqlite', check_same_thread=False)
kurzor = conn.cursor()
kurzor.execute("DROP TABLE IF EXISTS uporabniki.sqlite")
kurzor.execute('''
    CREATE TABLE IF NOT EXISTS uporabniki(
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Username VARCHAR(100),
        Email VARCHAR(100),
        Password TEXT NOT NULL
    )
''')
conn.commit()

app = Flask(__name__)
app.secret_key = "sw_the_goat123"

@app.route("/", methods=["GET", "POST"])
def home_page():
    if 'username' not in session:
        return render_template("signup.html")
    return render_template("index.html", username=session['username'])
    
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        if not username or not password:
            return jsonify({"success": False, "error": "Username and password are required."})
        hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        kurzor.execute("""INSERT INTO uporabniki (Username, Email, Password) VALUES (:username, :email, :password)""", {"username": username, "email": email, "password": hash})
        conn.commit()
        return jsonify({"success": True})
    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        kurzor.execute("SELECT Username, Password FROM uporabniki WHERE username = :username", {"username": username})
        row = kurzor.fetchone()
        if row and bcrypt.checkpw(password.encode("utf-8"), row[1]):
            session['username'] = username
            return jsonify({"success": True})
        else:
            return jsonify({"success": False, "error": "Invalid username or password."})
    return render_template("login.html")

@app.route("/logout")
def logout_page():
    session.pop('username', None)
    return redirect(url_for('login'))

app.run(debug=True)