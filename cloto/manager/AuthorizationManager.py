__author__ = 'gjp'
from keystoneclient.exceptions import AuthorizationFailure, Unauthorized, InternalServerError
import json


class AuthorizationManager():
    """This class provides methods to manage authorization.
    """
    myClient = None

    def generate_adminToken(self, username, password, url):
        """This method generates an admin token."""
        try:
            admin_client = self.myClient.Client(username=username, password=password, auth_url=url)
            return admin_client.auth_token
        except AuthorizationFailure as auf:
            raise(auf)
        except Unauthorized as unauth:
            raise(unauth)

    def checkToken(self, admin_token, token, tenant_id, url):
        """checks if a token is valid against a url using an admin token."""
        print("Starting Authentication of token %s " % token)
        admin_client = self.myClient.Client(token=admin_token, endpoint=url)
        try:
            auth_result = admin_client.tokens.authenticate(token=token, tenant_id=tenant_id)

            print("1. %s" % auth_result)
            print("2. %s" % admin_client.auth_token)
            if auth_result:
                if tenant_id == auth_result.tenant["id"]:
                    print('The token is valid')
                else:
                    raise Unauthorized("Token is not valid for specified tenant %s" % tenant_id)
        except Unauthorized as unauth:
            raise unauth
        except InternalServerError as internalError:
            raise AuthorizationFailure("Token could not have enough permissions to access tenant: %s" % tenant_id)
        except Exception as ex:
            raise ex
