from flask import Flask, render_template
import requests

app = Flask(__name__)


@app.route('/')
def main():
    response = requests.get("https://dog.ceo/api/breeds/image/random").json()
    image_url = response['message']
    return render_template('index.html', image_url=image_url)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')