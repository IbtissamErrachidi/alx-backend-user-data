#!/usr/bin/env python3
"""
Flask app
"""
from flask import Flask, request, jsonify
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"])
def home():
    """Handle GET request to the root endpoint."""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def register_user():
    """Handle user registration."""
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        return jsonify({"message": "email and password are required"}), 400

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError as e:
        return jsonify({"message": str(e)}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
