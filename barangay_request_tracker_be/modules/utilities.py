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

        logger.warning(f"Verifying Headers - x-api-key: {x_api_key}, x-brgy-code: {x_brgy_code}")   

        return x_api_key == current_app.config['API_KEY'] and x_brgy_code == current_app.config['BRGY_CODE']
    except Exception as e:
        return False
    
def VerifyTimestamp(data):
    try:
        payloadTimestamp = data['timestamp']
        convertedPayloadTimestamp = datetime.datetime.fromtimestamp(payloadTimestamp/1000) # convert payload time

        currentTime= datetime.datetime.now() # current time

        timeDiff = currentTime - convertedPayloadTimestamp # difference between time
        timeDiffSeconds = timeDiff.total_seconds() 
        timeDiffMinutes = timeDiffSeconds / 60 # get difference time in minutes

        validTimestamp = False

        if timeDiffSeconds <= 5:
            validTimestamp = True

        logger.warning("APILog: VerifyTimestamp. Valid: {isValid}. Difference in seconds: {diffTime}".format(isValid=validTimestamp,diffTime=timeDiffSeconds))
        return True #always return true for testing, still need to adjust time difference allowance
    except Exception as e:
        logger.error(f"VerifyTimestamp Exception: {e}")
        return False