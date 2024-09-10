#!/usr/bin/env python3
"""
Defines a basic flask app
"""


from flask import Flask, jsonify, request, abort, redirect, url_for
from auth import Auth
from sqlalchemy.orm.exc import NoResultFound


app = Flask(__name__)
AUTH = Auth()


@app.errorhandler(401)
def unauthorized(error):
    """
    Hnadles unautrhorized access
    """
    return jsonify({"error": "Wrong username or password"}), 401


@app.route("/", methods=["GET"], strict_slashes=False)
def index():
    """
    Basic index page
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users():
    """
    Registers user by saving in a database
    """
    email = request.form.get("email")
    if not email:
        return jsonify({"error": "Email missing"}), 400
    password = request.form.get("password")
    if not password:
        return jsonify({"error": "Password missing"}), 400
    try:
        user = AUTH.register_user(email, password)

        return jsonify({
            "email": user.email, "message": "user created"
        })
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login():
    """
    Handles login
    """
    email = request.form.get("email")
    password = request.form.get("password")
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie("session_id", session_id)
        return response
    else:
        abort(401)


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout():
    """
    Destroys the current user's session and redirect to index page
    """
    session_id = request.cookies.get("session_id")

    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    AUTH.destroy_session(user_id=user.id)
    return redirect(url_for("index"))


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile():
    """
    Returns the current user
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
