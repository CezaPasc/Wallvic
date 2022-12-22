import threading
from flask import Flask, render_template

import config
from wall.server import Server

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/draw")
def draw():
    return render_template("draw.html", size=config.size)

@app.route("/tetris")
def tetris():
    return render_template("tetris.html")


@app.route("/snake")
def snake():
    return render_template("snake.html")

if __name__ == "__main__":
    server = Server()
    threading.Thread(target=app.run, args=("0.0.0.0", 4200)).start()
    #app.run(host="0.0.0.0", port=4200)
    server.run()
