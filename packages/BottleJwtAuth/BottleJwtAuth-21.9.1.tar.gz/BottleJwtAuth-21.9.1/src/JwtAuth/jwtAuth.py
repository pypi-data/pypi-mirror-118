import os
from JwtEncoder import JwtEncoder
from .bottle_utils import (
            _Log, 
            UnauthorizedError, 
            BadRequestError, 
            request
        )

DEBUG = os.environ.get('DEBUG',False)

class JwtAuth:
    
    api = 2
    name = 'JwtAuth'

    def __init__(self, jwt_config, issuer, audience, url_prefix='/', log=_Log(), **kwargs):

        if url_prefix[-1] != '/':
            raise Exception('JwtAuth: url_prefix must end in "/"')

        self.url_prefix = url_prefix
        self.name = url_prefix
        self.audience = audience
        self.logger = log
        self.issuer = issuer

        self.jwt = JwtEncoder(jwt_config=jwt_config)


    def setup(self, app):

        for plugin in app.plugins:
            
            if isinstance(plugin, JwtAuth):

                if self.url_prefix in plugin.url_prefix  or plugin.url_prefix in self.url_prefix:
                    # Overlapping url_prefix
                    emsg = f'\nJwtAuth: Error - Overlapping URL prefixes \'{self.url_prefix}\' and \'{plugin.url_prefix}\''
                    raise Exception(emsg)

        self.logger.info(f'JwtAuth: Plugin installed for path {self.url_prefix}')


    def close(self):
        pass


    def apply(self, f, route):
        """ Check and apply prefix route """

        if route.rule.startswith(self.url_prefix):
            # This is a protected route.
            # apply any route restrictions first (referse order of checks)
            f = self.__apply_require_claim(f, route)
            f = self.__apply_require_scope(f, route)

            self.logger.debug(f'JwtAuth: prefix \'{self.name}\' audience validation applied to {route.rule}')

            # Apply audience route validation
            def _wrapper(*args, **kwargs):

                if tok := self._get_request_token():

                    if self._validate_token(tok):
                        # successful token validation
                        return f (*args, **kwargs) 
                    else:
                        return UnauthorizedError('Token error')
                else:
                    return BadRequestError('Malformed or missing Auth header')

            _wrapper.__name__ = f.__name__
            return _wrapper

        return f


    def __apply_require_scope(self, f, route):
        """ Require scopes on a route """

        if required_scope := route.config.get('scp'):
            
            self.logger.debug(f'JwtAuth: applying scope requirement on {route.rule}')

            def _wrapper(*args, **kwargs):
                # Validate scope 

                payload = request.token_payload
                payload_scope = payload.get('scp') or payload.get('scope')
                
                testok = True 
                if payload_scope is None:
                    # token doesn't have scp or scope
                    testok = False

                elif type(required_scope) is str and required_scope not in payload_scope:
                    # single scope required and is not present
                    testok = False

                elif type(required_scope) is list:
                    # multiple required scopes (e.g. scp=['email','user.read']
                    # All required scope values must be present.

                    for req_scp in required_scope:
                        if req_scp not in payload_scope:
                            testok = False
                            break
                
                if testok:
                    # required scopes are satisfied
                    return f(*args, **kwargs)

                return UnauthorizedError(f'Insufficient scope - requires: \'{required_scope}\'')

            _wrapper.__name__ = f.__name__
            return _wrapper
        
        # No wrapper
        return f


    def __apply_require_claim(self, f, route):
        """ Require claims on a route """

        claim = 'claim'
        
        if route.config.get(claim, False):
            
            self.logger.debug(f'JwtAuth: applying claim restricition on {route.rule}')

            # Build required claim list from config namespace
            req_claim_list = {}
            for key in route.config.get(claim):
                req_claim_list[key] = route.config[claim + '.' + key]

            def _claim_required(*args, **kwargs):
                """ Require claim/value match """

                payload = request.token_payload
                
                # check each claim to test
                for claim, value in req_claim_list.items():
                    # For every claim, the token must match at least one value

                    if claim not in payload or \
                        not test_attrs(payload[claim], value):

                        return UnauthorizedError('Missing one or more required claims')
                
                # all tests have passed to get here
                return f(*args, **kwargs)

            _claim_required.__name__ = f.__name__
            return _claim_required

        else:
            return f


    def _get_request_token(self):
        """ Retrieve jwt from request Authroization Header """

        auth_header = request.headers.get('Authorization')

        if auth_header and 'Bearer' in auth_header:

            token = auth_header.split(' ')[-1]
            if len(token.split('.')) == 3:
                
                # looks like a token
                return token

        # Meh.. bad or missing token
        return None


    def _validate_token(self, token):
        """ Verify JWT token """
        
        try:
            payload = self.jwt.decode(token, issuer=self.issuer, audience=self.audience)

            # add the payload to the request context
            request.token_payload = payload

        except Exception as e:
            self.logger.info(f'Token validation failed {str(e)}')
            return None

        return payload

#
# Helper routines
#
def test_attrs(challenge, standard):
    """
    test_attrs()

    Compare list or val the standard.
    
    - return True if at least one item from chalange list is in standard list
    - False if no match
    """

    stand_list = standard if type(standard) is list else [standard]
    chal_list = challenge if type(challenge) is list else [challenge]

    for chal in chal_list:
        if chal in stand_list:
            return True
    return False

