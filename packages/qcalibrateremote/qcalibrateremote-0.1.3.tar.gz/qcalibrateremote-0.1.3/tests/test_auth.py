from qcalibrateremote.grpc import combineKeyAndSecret, splitKeyAndSecret
from cuid import cuid
from icecream import ic

def test_combine_and_split():
    key = cuid()
    secret = cuid()
    ic(key, secret)
    
    keyAndSecret = combineKeyAndSecret(client_key=key, client_secret=secret)
    ic(keyAndSecret)
    (k,s) = splitKeyAndSecret(keyAndSecret)
    assert key == k
    assert secret == s
