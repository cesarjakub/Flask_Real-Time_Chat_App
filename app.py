from flask import Flask, render_template, session, request, redirect, url_for, flash
from dotenv import load_dotenv
from flask_mysqldb import MySQL
import hashlib
import os

app = Flask(__name__)

app.secret_key = os.getenv('TOKEN')

app.config['MYSQL_DB'] = os.getenv('DB_NAME')
app.config['MYSQL_HOST'] = os.getenv('DB_HOST')
app.config['MYSQL_USER'] = os.getenv('DB_USER')

mysql = MySQL(app)

load_dotenv()

@app.route("/")
def home_page():
    return render_template("homepage.html")

@app.route("/registration",  methods=["POST", "GET"])
def register():
    if request.method == "POST":
        username = request.form["Name"]
        email = request.form["Email"]
        password = request.form["Password"]
        password_confirm = request.form["Password_Confirm"]

        password_hash = hash_password(password)
        password_confirm_hash = hash_password(password_confirm)


        if password_hash == password_confirm_hash:
            cursor = mysql.connection.cursor()
            cursor.execute("INSERT INTO users (name, email, password) VALUES(%s, %s, %s)", (username, email, password_hash))
            mysql.connection.commit()
            cursor.close()
            return redirect(url_for("login"))
        else:
            flash('Passwords do not match. Please try again.', 'warning')
            return render_template("registerform.html")
    else:
        return render_template("registerform.html")

@app.route("/login")
def login():
    return render_template("loginform.html")

@app.route("/chat")
def chat():
    return render_template("chat.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

def hash_password(password):
    salt = "salted by kuba"
    password_with_salt = password + salt
    hashed_password = hashlib.sha256(password_with_salt.encode()).hexdigest()
    return hashed_password

if __name__ == '__main__':
    app.run(debug=True)