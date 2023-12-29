from flask import Flask, render_template, session, request, redirect, url_for, flash, jsonify, abort
from flask_socketio import SocketIO, join_room, leave_room
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

socketio = SocketIO(app)

load_dotenv()

#restapi routes
@app.route('/api/chat/', methods=['GET'])
def get_all_chat_posts():
    if "user" not in session:
        return redirect(url_for("home_page"))

@app.route('/api/chat/<int:id>', methods=['GET'])
def get_chat_post(id):
    if "user" not in session:
        return redirect(url_for("home_page"))
    
@app.route('/api/chat/', methods=['POST'])
def add_chat_post():
    if "user" not in session:
        return redirect(url_for("home_page"))

    
@app.route('/api/chat/<int:id>', methods=['DELETE'])
def delete_chat_post(id):
    if "user" not in session:
        return redirect(url_for("home_page"))

            
@app.route('/api/chat/<int:id>', methods=['PATCH'])
def update_chat_post(id):
    if "user" not in session:
        return redirect(url_for("home_page"))


#web routes
@app.route("/")
def home_page():
    return render_template("homepage.html")

@app.route("/registration", methods=["POST", "GET"])
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

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form["Email"]
        password = request.form["Password"]

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()

        if user and check_password(password, user[3]) and check_email(email, user[2]):
            session["user"] = user
            return redirect(url_for("chat"))
        else:
            flash("Password or email is incorrect", "warning")
            return render_template("loginform.html")
    else:
        return render_template("loginform.html")

def check_password(user_pass, db_pass):
    hash_user_pass = hash_password(user_pass)
    return hash_user_pass == db_pass
def check_email(user_email, db_email):
    return user_email == db_email

@app.route("/chat")
def chat():
    if "user" in session:
        return render_template("chat.html")
    else:
      
        return redirect(url_for("home_page"))

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home_page"))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

def hash_password(password):
    salt = "salted by kuba"
    password_with_salt = password + salt
    hashed_password = hashlib.sha256(password_with_salt.encode()).hexdigest()
    return hashed_password

#socket IO
@socketio.on('join')
def handle_join(data):
    user = session["user"]
    room = data['room']
    join_room(room)
    socketio.emit('mm', {'msg': user[1]+' has joined the room'}, room=room)

@socketio.on('leave')
def handle_leave(data):
    user = session["user"]
    room = data['room']
    leave_room(room)
    socketio.emit('mm', {'msg': user[1]+' has left the room'}, room=room)

@socketio.on('message')
def handle_message(data):
    user = session["user"]
    room = data['room']
    message = data['msg']
    socketio.emit('mm', {'msg': user[1]+ ": " +message}, room=room)

if __name__ == '__main__':
    socketio.run(app, debug=True)