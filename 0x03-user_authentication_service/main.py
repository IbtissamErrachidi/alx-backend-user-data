#!/usr/bin/env python3
"""
Main file
"""
import requests


def register_user(email: str, password: str) -> None:
    """
    Test for registering a new user with valid email and password.
    """
    response = requests.post(
        "http://localhost:5000/users",
        data={"email": email, "password": password}
    )
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "user created"}


def log_in_wrong_password(email: str, password: str) -> None:
    """
    Test for logging in with an incorrect password.
    """
    response = requests.post(
        "http://localhost:5000/sessions",
        data={"email": email, "password": password}
    )
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """
    Test for logging in with a valid email and password to retrieve session_id.
    """
    response = requests.post(
        "http://localhost:5000/sessions",
        data={"email": email, "password": password}
    )
    assert response.status_code == 200
    return response.cookies.get("session_id")


def profile_unlogged() -> None:
    """
    Test for profile access without being logged in (no session_id).
    """
    response = requests.get("http://localhost:5000/profile")
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """
    Test for profile access with a valid session_id.
    """
    cookies = {"session_id": session_id}
    response = requests.get(
        "http://localhost:5000/profile",
        cookies=cookies
    )
    assert response.status_code == 200


def log_out(session_id: str) -> None:
    """
    Test for logging out with a valid session_id.
    """
    cookies = {"session_id": session_id}
    response = requests.delete(
        "http://localhost:5000/sessions",
        cookies=cookies
    )
    assert response.status_code == 200


def reset_password_token(email: str) -> str:
    """
    Test for generating a reset password token with a valid email.
    """
    response = requests.post(
        "http://localhost:5000/reset_password",
        data={"email": email}
    )
    assert response.status_code == 200
    return response.json().get("reset_token")


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    Test for updating the password using a valid reset token.
    """
    response = requests.put(
        "http://localhost:5000/reset_password",
        data={
            "email": email,
            "reset_token": reset_token,
            "new_password": new_password
        }
    )
    assert response.status_code == 200


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
