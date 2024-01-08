from flask import Flask, render_template, session, request, redirect, url_for, flash, jsonify, abort
from flask_socketio import SocketIO, join_room, leave_room
from dotenv import load_dotenv
from flask_mysqldb import MySQL
import logging
from logging.handlers import RotatingFileHandler
import hashlib
import os

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv('TOKEN')

app.config['MYSQL_DB'] = os.getenv('DB_NAME')
app.config['MYSQL_HOST'] = os.getenv('DB_HOST')
app.config['MYSQL_USER'] = os.getenv('DB_USER')

mysql = MySQL(app)

socketio = SocketIO(app)


app.logger.setLevel(logging.ERROR)

error_handler = RotatingFileHandler('logs/error.log', maxBytes=10240, backupCount=5)
error_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))

app.logger.addHandler(error_handler)

app.logger.setLevel(logging.INFO)

info_handler = RotatingFileHandler('logs/info.log', maxBytes=10240, backupCount=5)
info_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))

app.logger.addHandler(info_handler)



#restapi routes
#vracení všech zpráv ze všech chat roomů
@app.route('/api/chat/', methods=['GET'])
def get_all_chat_posts():
    if "user" not in session:
        app.logger.info(f'Error: unauthorized access.')
        return redirect(url_for("home_page"))
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT users.name, users.email, message.MessageText, message.RoomID, message.Timestamp FROM message INNER JOIN users ON message.SenderID = users.id ORDER BY message.RoomID ")
    msg_post = cursor.fetchall()
    if msg_post:
        return jsonify(msg_post)
    else:
        return abort(404)

#vracení všech zpráv vybraného uživatele
@app.route('/api/chat/<name>', methods=['GET'])
def get_chat_posts_by_user(name):
    if "user" not in session:
        app.logger.info(f'Error: unauthorized access.')
        return redirect(url_for("home_page"))

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT users.name, users.email, message.MessageText, message.RoomID, message.Timestamp FROM message INNER JOIN users ON message.SenderID = users.id WHERE users.name = %s", (name,))
    msg_post = cursor.fetchall()
    if msg_post:
        return jsonify(msg_post)
    else:
        return abort(404)


#vracení všech zpráv vybrané chat room
@app.route('/api/chat/<int:id>', methods=['GET'])
def get_chat_post_by_chat_room(id):
    if "user" not in session:
        app.logger.info(f'Error: unauthorized access.')
        return redirect(url_for("home_page"))
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT users.name, users.email, message.MessageText, message.RoomID, message.Timestamp FROM message INNER JOIN users ON message.SenderID = users.id WHERE message.RoomID = %s", (id,))
    msg_post = cursor.fetchall()
    if msg_post:
        return jsonify(msg_post)
    else:
        return abort(404)
    
#vracení všech zpráv obsahujících vybrané slovo (case insensetive)
@app.route('/api/chat/word/<word>', methods=['GET'])
def get_chat_posts_by_word(word):
    if "user" not in session:
        app.logger.info(f'Error: unauthorized access.')
        return redirect(url_for("home_page"))
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT message.MessageText FROM message WHERE message.MessageText LIKE %s", ('%' + word + '%',))
    msg_post = cursor.fetchall()
    print(msg_post)
    print("AA")
    if msg_post:
        return jsonify(msg_post)
    else:
        return abort(404)

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
        app.logger.info(f'Error: unauthorized access.')
        return redirect(url_for("home_page"))

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home_page"))

def hash_password(password):
    salt = "salted by kuba"
    password_with_salt = password + salt
    hashed_password = hashlib.sha256(password_with_salt.encode()).hexdigest()
    return hashed_password

#errors
@app.errorhandler(400)
def bad_request(e):
    app.logger.error(f'Bad Request: {e}')
    return render_template('400.html'), 400

@app.errorhandler(401)
def unauthorized(e):
    app.logger.error(f'Unauthorized: {e}')
    return render_template('401.html'), 401

@app.errorhandler(403)
def forbidden(e):
    app.logger.error(f'Forbidden: {e}')
    return render_template('403.html'), 403

@app.errorhandler(404)
def page_not_found(e):
    app.logger.info(f'Not Found: {e}')
    return render_template('404.html'), 404

@app.errorhandler(405)
def method_not_allowed(e):
    app.logger.info(f'Method Not Allowed: {e}')
    return render_template('405.html'), 405

@app.errorhandler(500)
def internal_server_error(e):
    app.logger.info(f'Internal Server Error: {e}')
    return render_template('500.html'), 500


#socket IO
@socketio.on('join')
def handle_join(data):
    user = session["user"]
    room = data['room']
    join_room(room)
    socketio.emit('mm', {'user': 'System','msg': user[1]+' has joined the room'}, room=room)

    messages = get_messages_for_room(room)

    socketio.emit('load_messages', {'messages': messages}, room=room)

def get_messages_for_room(room):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT users.name, message.MessageText from users INNER JOIN message ON users.id = message.SenderID WHERE message.RoomID = %s;", (room,))
    msg_post = cursor.fetchall()
    if msg_post:
        return msg_post
    else:
        return abort(404)

@socketio.on('leave')
def handle_leave(data):
    user = session["user"]
    room = data['room']
    leave_room(room)
    socketio.emit('mm', {'user': 'System','msg': user[1]+' has left the room'}, room=room)

@socketio.on('message')
def handle_message(data):
    user = session["user"]
    room = data['room']
    message = data['msg']
    socketio.emit('mm', {'user': user[1], 'msg': message}, room=room)
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO message(SenderID, MessageText, RoomID) VALUES(%s, %s, %s)", (user[0], message, room))
    mysql.connection.commit()
    cursor.close()

if __name__ == '__main__':
    socketio.run(app, debug=True)