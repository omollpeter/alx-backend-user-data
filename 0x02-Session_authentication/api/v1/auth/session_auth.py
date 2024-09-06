#!/usr/bin/env python3
"""
Contains class for implementing session based authentication
"""


from api.v1.auth.auth import Auth
from uuid import uuid4
from models.user import User
from api.v1.views import app_views
from flask import request, jsonify
import os


class SessionAuth(Auth):
    """
    Implements session based authentication
    """

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates session id for user id
        """
        if not user_id:
            return None
        if type(user_id) is not str:
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Returns a user id based on a session id
        """
        if not session_id:
            return None
        if type(session_id) is not str:
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        Returns a user instance based on cookie value
        """
        session_id = self.session_cookie(request)
        if not session_id:
            return None
        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return None
        return User.get(user_id)


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
