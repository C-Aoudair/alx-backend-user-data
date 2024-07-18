#!/usr/bin/env python3
"""Flask app"""

from auth import Auth
from flask import Flask, jsonify, request, abort

app = Flask(__name__)
AUTH = Auth()


@app.route("/", strict_slashes=False)
def index():
    """index route"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users():
    """Users regestration route"""
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already exists"})


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login():
    """Login route"""
    email = request.form.get("email")
    password = request.form.get("password")

    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie("session_id", session_id)
        return response
    abort(401)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
