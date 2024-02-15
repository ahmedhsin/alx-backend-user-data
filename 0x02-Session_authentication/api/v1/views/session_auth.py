#!/usr/bin/env python3
""" Module of auth views
"""
from os import getenv
from flask import jsonify, request, make_response, abort
from api.v1.views import app_views
from models.user import User


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def logout() -> str:
    """route to handel the logout"""
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login_route() -> str:
    """login to the sys"""
    email = request.form.get('email')
    passwd = request.form.get('password')
    if email is None or email == '':
        return jsonify({"error": "email missing"}), 400
    if passwd is None or passwd == '':
        return jsonify({"error": "password missing"}), 400
    user = User.search({'email': email})
    if len(user) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    user = user[0]
    conf = User.is_valid_password(user, passwd)
    if not conf:
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth
    cookie = auth.create_session(user.id)
    _my_session = getenv('SESSION_NAME')
    res = make_response(user.to_json())
    res.set_cookie(_my_session, cookie)
    return res
