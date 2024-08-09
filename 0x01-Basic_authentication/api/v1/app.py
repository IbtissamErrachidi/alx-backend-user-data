#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv

from flask import Flask, abort, jsonify, request
from flask_cors import CORS

from api.v1.views import app_views

app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None
AUTH_TYPE = getenv("AUTH_TYPE")
if AUTH_TYPE == "auth":
    from api.v1.auth.auth import Auth

    auth = Auth()
elif AUTH_TYPE == "basic_auth":
    from api.v1.auth.basic_auth import BasicAuth

    auth = BasicAuth()


@app.before_request
def before_request() -> str:
    """Handle the Authentication"""
    if not auth or not auth.require_auth(
        request.path,
        ["/api/v1/status/", "/api/v1/unauthorized/", "/api/v1/forbidden/"],
    ):
        return
    if auth.authorization_header(request) is None:
        return abort(401)
    if auth.current_user(request) is None:
        return abort(403)


@app.errorhandler(404)
def not_found(error) -> str:
    """Not found"""
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """Un authorized"""
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """For bidden """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=int(port))
