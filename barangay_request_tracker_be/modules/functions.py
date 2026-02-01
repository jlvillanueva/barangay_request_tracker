from base64 import b64decode, b64encode
import hashlib
import os

def GenerateSaltKey(phrase):
    salt = os.urandom(37)
    key = hashlib.pbkdf2_hmac('sha256', phrase.encode('utf-8'), salt, 100000)
    dbsalt = (b64encode(salt)).decode('utf8')
    dbkey = (b64encode(key)).decode('utf8')
    reply = {
        "salt": dbsalt,
        "key": dbkey,
    }
    return reply

def VerifyPhrase(phrase, salt, key):
    encryptedPhrase = hashlib.pbkdf2_hmac('sha256', phrase.encode('utf8'), b64decode(salt), 100000)
    phraseValidity = encryptedPhrase == b64decode(key)
    return phraseValidity