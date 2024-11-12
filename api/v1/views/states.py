#!/usr/bin/python
"""makes a new webframwork"""
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests


app = Flask("__name__")


db = SQLAlchemy(app)


class State(db.Model):
    __tablename__ = "states"

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