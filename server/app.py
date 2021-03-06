import random
from flask import request
import time
import flask
from flask import Flask
from moves import *
from board import Board
from flask_sqlalchemy import SQLAlchemy
import chess

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
    fen = request.json["fen"]
    board = chess.Board(fen)
    print(board)
    print(board.board_fen, fen)
    index = 0 
    best = get_best_move(moves, turn, board)
    print(best)
    return flask.jsonify(best)

# request all stored fen strings from database 
@app.route('/positions', methods=["GET"])
def get_positions():
    ret = [{"name": f.name, "fen_string": f.fen_string} for f in Fen.query.all()]
    return flask.jsonify({"result": ret})

# Deletes all positions from databse
@app.route('/delete_all', methods=["GET"])
def delete_all():
    for f in Fen.query.all():
        db.session.delete(f)
    db.session.commit()
    return flask.jsonify({"result": "success"})

# saves a new fen string to the databse
@app.route('/save_pos', methods=["POST"])
def save_pos():
    fen = request.json["fen"]
    name = request.json["name"]
    new_fen = Fen(name=name, fen_string=fen)
    if Fen.query.filter_by(name=name).all():
        print("already saved name in databse")
        return flask.jsonify({"status": "failed"})
    db.session.add(new_fen)
    db.session.commit()
    return flask.jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(host="localhost", port="5000", debug=True)
