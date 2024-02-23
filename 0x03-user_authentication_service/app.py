#!/usr/bin/env python3
"""simple flask api application"""

from flask import Flask, jsonify, request, abort
from flask import make_response, redirect
from auth import Auth


AUTH = Auth()

app = Flask(__name__)


@app.route('/')
def hello_world() -> None:
    """entry point route"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users() -> None:
    """route for registerntion"""
    email = request.form.get('email')
    password = request.form.get('password')
    user = None
    try:
        user = AUTH.register_user(email, password)
    except Exception:
        return jsonify({"message": "email already registered"}), 400
    return jsonify({"email": f"{email}", "message": "user created"})


@app.route('/sessions', methods=['POST'])
def login() -> None:
    """login route"""
    email = request.form.get('email')
    password = request.form.get('password')
    valid = AUTH.valid_login(email, password)
    if not valid:
        abort(401)
    session_id = AUTH.create_session(email)
    res = make_response({"email": f"email", "message": "logged in"})
    res.set_cookie('session_id', session_id)
    return res


@app.route('/sessions', methods=['DELETE'])
def logout() -> str:
    """logout route"""
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        Auth.destroy_session(user.id)
        return redirect('/')
    abort(403)


@app.route('/profile', methods=['GET'])
def profile() -> None:
    """handle profle route"""
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": f"{user.email}"})
    abort(403)


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token() -> None:
    """reset password"""
    email = request.form.get('email')
    try:
        token = AUTH.get_reset_password_token(email)
        return jsonify({"email": f"{email}", "reset_token": f"{token}"})
    except ValueError:
        abort(403)


@app.route('/reset_password', methods=['PUT'])
def update_password():
    """update_password"""
    email = request.form.get('email')
    password = request.form.get('new_password')
    token = request.form.get('reset_token')

    try:
        AUTH.update_password(token, password)
        return jsonify({"email": email, "message": "Password updated"})
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
