import traceback

from flask import Blueprint, request, abort
from app.services.auth_services import generate_token, register_user, authenticate_user
from app.utils import logger
from app.utils.json_encoders import jsonify

api = Blueprint('auth_api', __name__, url_prefix='/auth')


@api.route('/login', methods=['GET'])
def login():
    try:
        if request.authorization:

            if authenticate_user(request.authorization["username"], request.authorization["password"]):
                return jsonify({
                    "token": generate_token(request.authorization["username"])
                }), 200
            else:
                return jsonify({
                    "msg": "The login credentials are either wrong or unavailable in the users database."
                }), 403
        else:
            return jsonify({
                "msg": "Username/Password not found in authorization header"
            }), 400
    except Exception as e:
        logger.exception(e)
        abort(500)


@api.route('/register', methods=['POST'])
def register_new_user():
    try:

        body = request.json

        if not body:
            return jsonify({
                "msg": "request json not found"
            }), 400

        if "username" not in body:
            return jsonify({
                "msg": "username not present in request body"
            }), 400

        if "password" not in body:
            return jsonify({
                "msg": "password not present in request body"
            }), 400

        result = register_user(body["username"], body["password"])

        return jsonify(result), 201

    except Exception as e:
        logger.exception(e)
        abort(500)
