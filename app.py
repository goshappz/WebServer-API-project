from flask import Flask, render_template, request, redirect
from data import db_session
from data.users import User
from flask_login import (LoginManager, login_user, logout_user, login_required, current_user)
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
db_session.global_init("db/users.db")
db_sess = db_session.create_session()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "Сначала войдите в аккаунт"


@login_manager.user_loader
def load_user(user_id):
    user = db_sess.get(User, int(user_id))
    db_sess.close()
    return user


@app.route('/')
def main():
    response = requests.get("https://dog.ceo/api/breeds/image/random").json()
    image_url = response['message']
    return render_template('index.html', image_url=image_url)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        ident = request.form.get("username_or_email").strip()
        password = request.form['password_login'].strip()
        if db_sess.query(User).filter(User.name == ident, User.password == password).first():
            login_user(db_sess.query(User).filter(User.name == ident).first())
            return redirect("/")
    return render_template("login.html")


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        email = request.form['email'].strip().lower()
        password = request.form['password'].strip()
        terms = request.form['terms']
        for user in db_sess.query(User).all():
            if user.email == email:
                return render_template('register.html', email_error="Этот адрес электронной почты уже используется")
        user = User()
        user.name = username
        user.email = email
        user.password = password
        db_sess.add(user)
        db_sess.commit()
        redirect("/")
    return render_template("register.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")

@login_required
@app.route("/profile")
def profile():
    return render_template("profile.html")
if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
