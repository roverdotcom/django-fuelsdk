import logging
import time

from FuelSDK import ET_Client
import jwt


class ConfigurableET_Client(ET_Client):
    """
    The base ET_Client class requires the configuration to be loaded from a
    file, this subclass allows the configuration to be specified at runtime.
    """
    def __init__(self, get_server_wsdl=False, debug=False, params=None):
        self.debug = debug
        if debug:
            logging.basicConfig(level=logging.INFO)
            logging.getLogger('suds.client').setLevel(logging.DEBUG)
            logging.getLogger('suds.transport').setLevel(logging.DEBUG)
            logging.getLogger('suds.xsd.schema').setLevel(logging.DEBUG)
            logging.getLogger('suds.wsdl').setLevel(logging.DEBUG)

        ## Read the config information out of config.python
        config = ConfigParser.RawConfigParser()
        config.read('config.python')
        self.client_id = config.get('Web Services', 'clientid')
        self.client_secret = config.get('Web Services', 'clientsecret')
        self.appsignature = config.get('Web Services', 'appsignature')
        wsdl_server_url = config.get('Web Services', 'defaultwsdl')
        self.auth_url = config.get('Web Services', 'authenticationurl')

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
