from base64 import b64encode, b64decode
from icecream import ic

GRPC_AUTH_HEADER = 'rpc-auth-header'

_ASCII = "ascii"

def splitKeyAndSecret(keyAndSecret):
    (client_key, client_secret) = b64decode(str.encode(keyAndSecret, _ASCII)).decode(_ASCII).split(':', 2)
    return client_key,client_secret

def combineKeyAndSecret(client_key, client_secret):
    return b64encode(f"{client_key}:{client_secret}".encode(_ASCII)).decode(_ASCII)
