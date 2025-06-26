from flask import Flask, session, render_template, jsonify, redirect, url_for, request
import sqlite3
import bcrypt

user_conn = sqlite3.connect('uporabniki.sqlite', check_same_thread=False)
user_cursor = user_conn.cursor()
user_cursor.execute('''
    CREATE TABLE IF NOT EXISTS uporabniki(
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Username VARCHAR(100),
        Email VARCHAR(100),
        Password TEXT NOT NULL
    )
''')
user_conn.commit()

task_conn = sqlite3.connect('tasks.sqlite', check_same_thread=False)
task_cursor = task_conn.cursor()
task_cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks(
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        UserID INT,
        Name VARCHAR(100),
        Description VARCHAR(1000),
        FOREIGN KEY (UserID) REFERENCES uporabniki(ID)
    )
''')
task_conn.commit()

app = Flask(__name__)
app.secret_key = "sw_the_goat123"

@app.route("/", methods=["GET", "POST"])
def home_page():
    if 'username' not in session:
        return render_template("signup.html")
    user_cursor.execute("SELECT ID from uporabniki WHERE username = :username", {"username": session['username']})
    userRow = user_cursor.fetchone()
    UserID = userRow[0]
    task_cursor.execute("SELECT Name, Description FROM tasks WHERE UserID = :UserID", {"UserID": UserID})
    tasks = task_cursor.fetchall()
    return render_template("index.html", username=session['username'], tasks=tasks)
    
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        if username == "" or password == "":
            return jsonify({"success": False, "error": "Username and password are required."})
        hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user_conn.execute("""INSERT INTO uporabniki (Username, Email, Password) VALUES (:username, :email, :password)""", {"username": username, "email": email, "password": hash})
        user_conn.commit()
        return jsonify({"success": True})
    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == "" or password == "":
            return jsonify({"success": False, "error": "Username and password are required."})
        user_cursor.execute("SELECT Username, Password FROM uporabniki WHERE username = :username", {"username": username})
        row = user_cursor.fetchone()
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

@app.route("/addTask", methods=["GET", "POST"])
def addTask():
    if 'username' not in session:
        return render_template("signup.html")
    if request.method == "POST":
        user_cursor.execute("SELECT ID from uporabniki WHERE username = :username", {"username": session['username']})
        row = user_cursor.fetchone()
        UserID = row[0]
        print("Session username:", session['username'])
        print("Fetched user row:", UserID)
        taskName = request.form.get("taskName")
        taskDesc = request.form.get("taskDesc")
        task_cursor.execute("""INSERT INTO tasks (UserID, Name, Description) VALUES (:UserID, :taskName, :taskDesc)""", {"UserID": UserID, "taskName": taskName, "taskDesc": taskDesc})
        task_conn.commit()
        return jsonify({"success": True})
    return render_template("addTask.html")

app.run(debug=True)