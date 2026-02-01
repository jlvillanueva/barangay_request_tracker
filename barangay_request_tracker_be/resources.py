from collections import OrderedDict
from functools import wraps
import logging


from datetime import datetime

from modules.utilities import VerifyPayload
from flask_restful import Resource
from flask import json, request
from mobile_sql_alchemy import mobile_db

from models.mod_users import Users
from modules.functions import VerifyPhrase, GenerateSaltKey


# Logging config
logger = logging.getLogger(__name__)

def verify_payload():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                data = json.loads(request.data, object_pairs_hook=OrderedDict)


                dictdata = data.get('data')

                logger.warning(f"Verifying payload for data: {dictdata}")
            
                verifydata = VerifyPayload(dictdata)

                if not verifydata:
                    return {
                        'rc': 400,
                        'status': 'Invalid payload'
                    }, 400
            except Exception as e:
                logger.error(f"Payload verification failed: {e}")
                return {
                    'rc': 400,
                    'status': 'Invalid payload format'
                }, 400
            return func(*args, **kwargs)
        return wrapper
    return decorator

class OAuth2(Resource):
    @verify_payload()
    def post(self):
        return {
            'rc': 200,
            'status': 'OAuth2 Endpoint - Placeholder'
        }

class MobileLogin(Resource):
    @verify_payload()
    def post(self):
        data = request.get_json()
        logger.warning(f"User attempting login: {data.get('data').get('username')}")

        user = Users.query.filter_by(username=data.get('data').get('username')).first()

        password = data.get('data').get('password')

        if user and VerifyPhrase(password, user.password_salt, user.password_key):
            return {
                'rc': 201,
                'status': 'Login Successfully',
            }
        else:
            return {
                'rc': 401,
                'status': 'Invalid credentials',
            }

class MobileRegistration(Resource):
    def post(self):
        data = request.get_json()

        password = data.get('data').get('password')

        reply = GenerateSaltKey(password)

        user = Users(
            username=data.get('data').get('username'),
            firstName=data.get('data').get('firstName'),
            lastName=data.get('data').get('lastName'),
            phoneNumber=data.get('data').get('phoneNumber'),
            middleName=data.get('data').get('middleName'),
            role=data.get('data').get('role', 'RESIDENT'),
            createdAt=datetime.now(),
            password_salt=reply['salt'],
            password_key=reply['key'],
        )

        try:
            mobile_db.session.add(user)
            mobile_db.session.commit()
            # Fetch the user from the database to ensure data is from DB
            db_user = Users.query.filter_by(id=user.id).first()
            return {
                'rc': 201,
                'status': 'Registered Successfully',
                'clientid': db_user.id,
                'cpnumber': db_user.phoneNumber
            }, 201
        except Exception as e:
            mobile_db.session.rollback()
            logger.error(f"Registration failed: {e}")
            return {
                'rc': 401,
                'status': 'Registration Failed'
            }, 401