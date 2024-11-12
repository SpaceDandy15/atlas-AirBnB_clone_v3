#!/usr/bin/python3
"""makes a new webframwork"""
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests


app = Flask("__name__")


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///states.db'


db = SQLAlchemy(app)


class State(db.Model):
    __tablename__ = "states"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __init__(self, name):
        self.name = name

    @staticmethod
    def to_dict(state):
        return {"id": state.id, "name": state.name}


with app.app_context():
    db.create_all()


@app.route("/api/v1/states", methods=["GET"])
def all_states():
    states = State.query.all()
    return jsonify([State.to_dict(state) for state in states])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)