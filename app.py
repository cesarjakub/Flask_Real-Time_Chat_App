from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home_page():
    return render_template("homepage.html")

@app.route("/registration")
def register():
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

if __name__ == '__main__':
    app.run(debug=True)