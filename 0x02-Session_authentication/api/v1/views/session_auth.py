#!/usr/bin/env


from api.v1.views import app_views
from flask import request, jsonify
import os
from models.user import User


@app_views.route("/auth_session/login", methods=["POST"], strict_slashes=False)
def login():
    """
    Handles user login
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if not email:
        return jsonify({"error": "email missing" }), 400
    if not password:
        return jsonify({"error": "password missing" }), 400

    user_list = User.search({"email": email})
    if not user_list:
        return jsonify({"error": "no user found for this email"}), 404
    user = user_list[0]

    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    session_id = auth.create_session(request)
    output = jsonify(user.to_json())
    cookie_name = os.getenv("SESSION_NAME")
    output.set_cookie(cookie_name, str(session_id))
    return output
