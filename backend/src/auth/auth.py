import json
from flask import request, _request_ctx_stack, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen

AUTH0_DOMAIN = 'kcruz.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'coffee-shop'

# AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Auth Header


# @TODO implement get_token_auth_header() method (DONE)
'''
    it should attempt to get the header from the request
    it should raise an AuthError if no header is present
    it should attempt to split bearer and the token
    it should raise an AuthError if the header is malformed
    return the token part of the header
'''


def get_token_auth_header():
    if "Authorization" not in request.headers:
        raise AuthError({
            'code': 'Authorization not present in headers',
            'description': 'Unable to get authorization from header'
        }, 401)

    auth_header = request.headers["Authorization"]
    auth_header_split = auth_header.split(" ")

    if len(auth_header_split) != 2:
        raise AuthError({
            'code': 'header malformed',
            'description': 'authorization header length not equal to 2'
        }, 401)
    elif auth_header_split[0].lower() != "bearer":
        raise AuthError({
            'code': 'bearer keyword not found',
            'description': 'the bearer keyword not found in authorization '
                           'header'
        }, 401)

    token = auth_header_split[1]
    return token


# @TODO implement check_permissions(permission, payload) method (DONE)
#     @INPUTS
#         permission: string permission (i.e. 'post:drink')
#         payload: decoded jwt payload
'''
    it should raise an AuthError if permissions are not included in the 
    payload
        !!NOTE check your RBAC settings in Auth0
    it should raise an AuthError if the requested permission string is 
    not in the payload permissions array return true otherwise
'''


def check_permissions(permission, payload):
    if "permissions" not in payload:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permissions not included in JWT.'
        }, 400)

    if permission not in payload["permissions"]:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission not found.'
        }, 403)


# @TODO implement verify_decode_jwt(token) method (DONE)
#     @INPUTS
#         token: a json web token (string)
'''
    it should be an Auth0 token with key id (kid)
    it should verify the token using Auth0 /.well-known/jwks.json
    it should decode the payload from the token
    it should validate the claims
    return the decoded payload

    !!NOTE urlopen has a common certificate error described here: 
    https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
'''


def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    # print('This is jwks:', jwks)

    unverified_header = jwt.get_unverified_header(token)
    # print(f"Unverified Header: {unverified_header}")

    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }

    if rsa_key:
        try:
            # Use the key to validate the JWT
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer=f'https://{AUTH0_DOMAIN}/'
            )

            for key, value in payload.items():
                print(key, ": ", value)

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token is expired'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please check the audience'
                               'and issuer'
            }, 401)

        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
        'code': 'invalid_header',
        'description': 'Unable to find the appropriate key'
    }, 400)


# @TODO implement @requires_auth(permission) decorator method (DONE)
#     @INPUTS
#         permission: string permission (i.e. 'post:drink')
'''
    it should use the get_token_auth_header method to get the token
    it should use the verify_decode_jwt method to decode the jwt
    it should use the check_permissions method validate claims and check the 
    requested permission
    return the decorator which passes the decoded payload to the decorated
    method
'''


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            jwt = get_token_auth_header()
            try:
                payload = verify_decode_jwt(jwt)
            except:
                abort(401)

            check_permissions(permission, payload)

            return f(payload, *args, **kwargs)

        return wrapper

    return requires_auth_decorator
