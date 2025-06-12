from flask import Flask, session, render_template

app = Flask(__name__)

@app.route("/")
def home_page():
    if 'username' not in session:
        return render_template("signup.html")
    return render_template("index.html")
    
@app.route("/signup")
def signup():
    return render_template("signup.html")

app.run(debug=True)