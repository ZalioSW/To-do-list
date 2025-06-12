from flask import Flask, session, render_template, jsonify, redirect, url_for, request
import sqlite3

conn = sqlite3.connect('uporabniki')
kurzor = conn.cursor()
kurzor.execute('''
    CREATE TABLE IF NOT EXISTS uporabniki(
        ID INT PRIMARY KEY NOT NULL ,
        Username VARCHAR(100),
        Email VARCHAR(100),
        Password TEXT NOT NULL
    )
''')
conn.commit()
conn.close()

app = Flask(__name__)

@app.route("/")
def home_page():
    if 'username' not in session:
        return render_template("signup.html")
    return render_template("index.html")
    
@app.route("/signup", methods = ["GET", "POST"])
def signup():
    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]
    print(username)
    print(email)
    print(password)
    return render_template("signup.html")

@app.route("/login")
def login():
    return render_template("login.html")

app.run(debug=True)