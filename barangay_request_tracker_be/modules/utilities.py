from base64 import b64encode

import datetime
import json
import logging
import passlib.hash
import api as app

from flask import current_app, request

# Logging config
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def sort_payload(data):
    if isinstance(data, dict):
        return {k: sort_payload(data[k]) for k in sorted(data)}
    elif isinstance(data, list):
        return [sort_payload(item) for item in data]
    else:
        return data


def VerifyPayload(data):
    data = data

    validDigest = VerifyDigest(data)
    validHeaders = VerifyHeaders()
    validTimestamp = VerifyTimestamp(data)

    logger.warning(f"Payload Verification - Digest: {validDigest}, Headers: {validHeaders}, Timestamp: {validTimestamp}")

    return validDigest and validHeaders and validTimestamp

def VerifyDigest(data):

    try:
        data = dict(data)

        digest = data['digest']
        data.pop('digest', None)

        data = sort_payload(data)
        print(f'Pre-encode payload: {data}')
        payloadToVerify = json.dumps(data, separators=(',', ':'), ensure_ascii=False)
        print(f'Encoded payload: {b64encode(payloadToVerify.encode("utf-8")).decode("utf-8")}')
        payloadToVerify = b64encode(payloadToVerify.encode('utf-8')).decode('utf-8')
        salt = current_app.config.get('DIGEST_SALT')
        # Manual SHA-256 with salt and rounds (match Dart)
        digestMessage = passlib.hash.sha256_crypt.using(salt=salt, rounds=1000).hash(payloadToVerify)

        logger.warning(f"Step 9: Verifying Digest - Computed: {digestMessage}, Provided: {digest}")
        logger.error(f"Step 10: is Match: {digestMessage == digest}")
        return digestMessage == digest
    except Exception as e:
        logger.error(f"Exception in VerifyDigest: {e}")
        return False
    
def VerifyHeaders():
    try:
        x_api_key = request.headers.get('x-api-key') #application api key
        x_brgy_code = request.headers.get('x-brgy-code') #barangay code

        return x_api_key == current_app.config['API_KEY'] and x_brgy_code == current_app.config['BRGY_CODE']
    except Exception as e:
        return False
    
def VerifyTimestamp(data):
    try:
        timestamp = data['timestamp']

        current_timestamp = datetime.datetime.now()

        message_timestamp = datetime.datetime.fromisoformat(timestamp)

        time_difference = abs((current_timestamp - message_timestamp).total_seconds())
        return time_difference <= 5 * 60
    except Exception as e:
        return False