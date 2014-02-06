import logging
import time

from FuelSDK import ET_Client
import jwt


# https://code.exacttarget.com/question/there-any-cetificrate-install-our-server-access-et-api
PRODUCTION_WSDL_URL = 'https://webservice.exacttarget.com/etframework.wsdl'
PRODUCTION_AUTH_URL = 'https://auth.exacttargetapis.com/v1/requestToken?legacy=1'


class ConfigurableET_Client(ET_Client):
    """
    The base ET_Client class requires the configuration to be loaded from a
    file, this subclass allows the configuration to be specified at runtime.
    """
    def __init__(
            self,
            client_id,
            client_secret,
            appsignature=None,
            wsdl_server_url=PRODUCTION_WSDL_URL,
            auth_url=PRODUCTION_AUTH_URL,
            get_server_wsdl=False,
            debug=False,
            params=None):

        self.debug = debug
        if debug:
            logging.basicConfig(level=logging.INFO)
            logging.getLogger('suds.client').setLevel(logging.DEBUG)
            logging.getLogger('suds.transport').setLevel(logging.DEBUG)
            logging.getLogger('suds.xsd.schema').setLevel(logging.DEBUG)
            logging.getLogger('suds.wsdl').setLevel(logging.DEBUG)

        self.client_id = client_id
        self.client_secret = client_secret
        self.appsignature = appsignature
        wsdl_server_url = wsdl_server_url
        self.auth_url = auth_url

        self.wsdl_file_url = self.load_wsdl(wsdl_server_url, get_server_wsdl)

        ## get the JWT from the params if passed in...or go to the server to get it
        if params is not None and 'jwt' in params:
            decodedJWT = jwt.decode(params['jwt'], self.appsignature)
            jwt_user = decodedJWT['request']['user']
            self.authToken = jwt_user['oauthToken']
            self.authTokenExpiration = time.time() + jwt_user['expiresIn']
            self.internalAuthToken = jwt_user['internalAuthToken']

            if 'refreshToken' in jwt_user:
                self.refreshKey = jwt_user['refreshToken']
            self.build_soap_client()
            pass
        else:
            self.refresh_token()
