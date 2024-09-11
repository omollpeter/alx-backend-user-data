#!/usr/bin/python3
"""
Tests the API endpoints
"""


import requests


url = "http://0.0.0.0:5000"


def register_user(email: str, password: str) -> None:
    """
    Tests whether users can be registered successfully
    """
    data = {
        "email": email,
        "password": password
    }

    req_url = f"{url}/users"
    response = requests.post(url=req_url, data=data)

    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "user created"}


def log_in_wrong_password(email: str, password: str) -> None:
    """
    Tests whether wrong login credentials raises error
    """
    data = {
        "email": email,
        "password": password
    }

    req_url = f"{url}/sessions"
    response = requests.post(url=req_url, data=data)

    assert response.status_code == 401
    assert response.json() == {"error": "Wrong username or password"}


def log_in(email: str, password: str) -> str:
    """
    Tests whether a user with right credentials is blogged in successfully
    """
    data = {
        "email": email,
        "password": password
    }

    req_url = f"{url}/sessions"
    response = requests.post(url=req_url, data=data)

    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "logged in"}

    sess_id = response.cookies.get_dict().get("session_id")
    return sess_id


def profile_unlogged() -> None:
    """
    Test if accessing profile without logging in fails
    """
    req_url = f"{url}/profile"
    response = requests.get(url=req_url)

    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """
    Test if accessing profile when logged in is successful
    """
    cookies = {
        "session_id": session_id
    }
    req_url = f"{url}/profile"
    response = requests.get(url=req_url, cookies=cookies)

    assert response.status_code == 200


def log_out(session_id: str) -> None:
    """
    Tests user logout
    """
    cookies = {
        "session_id": session_id
    }
    req_url = f"{url}/sessions"
    response = requests.delete(url=req_url, cookies=cookies)

    assert response.status_code == 200


def reset_password_token(email: str) -> str:
    """
    Tests whether password reset token is generated
    """
    data = {"email": email}

    req_url = f"{url}/reset_password"
    response = requests.post(url=req_url, data=data)

    assert response.status_code == 200
    return response.json().get("reset_token")


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    Tests whether user password is updated successfully
    """
    data = {
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password
    }

    req_url = f"{url}/reset_password"
    response = requests.put(url=req_url, data=data)

    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "Password updated"}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
