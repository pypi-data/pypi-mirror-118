from grpc import AuthMetadataPlugin
from .grpc import GRPC_AUTH_HEADER


class GrpcAuth(AuthMetadataPlugin):
    """Class implents a metadata plugin adding access token header as call level security

    Parameters
    ----------
    grpc : [type]
        [description]
    """
    def __init__(self, token):
        self._token = token

    def __call__(self, context, callback):
        callback(((GRPC_AUTH_HEADER, self._token),), None)
