from flask import Flask, render_template, request
from data import db_session
from data.users import User
import requests

app = Flask(__name__)

db_session.global_init("db/users.db")
db_sess = db_session.create_session()


@app.route('/')
def main():
    response = requests.get("https://dog.ceo/api/breeds/image/random").json()
    image_url = response['message']
    return render_template('index.html', image_url=image_url)


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        email = request.form['email'].strip()
        password = request.form['password'].strip()
        terms = request.form['terms'].strip()
        for user in db_sess.query(User).all():
            if user.email == email:
                return render_template('register.html', email_error="Этот адрес электронной почты уже используется")
        user = User()
        user.name = username
        user.email = email
        user.password = password
        db_sess.add(user)
        db_sess.commit()
    return render_template('register.html')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
