import random
from flask import request
import time
import flask
from flask import Flask
from moves import *
from board import Board
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
db = SQLAlchemy(app)


# Class to represent a fen string in database
class Fen(db.Model):
    name = db.Column(db.String(100), primary_key=True)
    fen_string = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"name: {self.name}, fen: {self.fen_string}"


# Recieves current board settup and calculate best move
@app.route('/hax', methods=["POST"])
def recv_pos():
    moves = request.json["moves"]
    turn = request.json["turn"]
    fen = request.json["fen"].split()[0]
    board = Board(fen)
    index = 0 
    best = get_best_move(moves, turn, board)
    print(board)
    return flask.jsonify(best)

# request all stored fen strings from database 
@app.route('/positions', methods=["GET"])
def get_positions():
    ret = [{"name": f.name, "fen_string": f.fen_string} for f in Fen.query.all()]
    return flask.jsonify({"result": ret})

# saves a new fen string to the databse
@app.route('/save_pos', methods=["POST"])
def save_pos():
    fen = request.json["fen"]
    new_fen = Fen(name="Random name here" + str(random.randrange(0,100000)), fen_string=fen)
    db.session.add(new_fen)
    db.session.commit()
    return flask.jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(host="localhost", port="5000", debug=False)
