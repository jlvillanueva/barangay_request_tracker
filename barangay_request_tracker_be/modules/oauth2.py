import string
from flask import current_app, request

import logging
import secrets

import jwt

from models.mod_users import Users
from modules.functions import VerifyPhrase

# Logging config
logger = logging.getLogger(__name__)


def generate_token():
    data = request.get_json()
    logger.warning(f"User attempting login: {data.get('data').get('username')}")

    user = Users.query.filter_by(username=data.get('data').get('username')).first()

    logger.warning(f"Fetched user from database: {user.firstName if user else 'None'}")

    password = data.get('data').get('password')

    if user and VerifyPhrase(password, user.password_salt, user.password_key):
        tokenidenty = {
            'userId': user.id,
            'clienKey': data.get('data').get('clientKey', None),
            'clientSecret': data.get('data').get('clientSecret', None),
        }

        access_token = jwt.encode(tokenidenty, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')

        logger.warning(f"Generated JWT Token for user {user.username}: {access_token}")

        return {
            'rc': 201,
            'status': 'Login Successfully',
            'clientId': user.id,
            'access_token': access_token,
            'userDetails': {
                'username': user.username,
                'firstName': user.firstName,
                'middleName': user.middleName,
                'lastName': user.lastName,
                'contactNumber': user.phoneNumber,
                'role': user.role,
            }
        }
    else:
        return {
            'rc': 401,
            'status': 'Invalid credentials',
        }
    return token