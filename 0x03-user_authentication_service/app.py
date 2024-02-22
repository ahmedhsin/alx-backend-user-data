#!/usr/bin/env python3
"""simple flask api application"""

from flask import Flask, jsonify, request
from auth import Auth


AUTH = Auth()

app = Flask(__name__)


@app.route('/')
def hello_world() -> None:
    """entry point route"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def register_route() -> None:
    """route for registerntion"""
    email = request.form.get('email')
    password = request.form.get('password')
    user = None
    try:
        user = AUTH.register_user(email, password)
    except Exception:
        return jsonify({"message": "email already registered"}), 400
    return jsonify({"email": f"{email}", "message": "user created"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
