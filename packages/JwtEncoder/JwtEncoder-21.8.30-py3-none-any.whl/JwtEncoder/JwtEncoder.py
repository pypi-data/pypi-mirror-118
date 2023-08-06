from secrets import token_bytes
import time

from cryptography.x509 import load_pem_x509_certificate
from cryptography.hazmat.primitives import serialization
import jwt

from .JWKS import Jwks

now = lambda ttl=0 : int(time.time()) + ttl

default_ttl = 3600

class JwtASym:
    """ Asymmetric encoded JWT """
    
    def __init__(self, jwt_config):
        
        self.iss = jwt_config.get('iss')
        self.pub_key = jwt_config.get('pubkey')
        self.priv_key = jwt_config.get('privkey')
        self.alg = jwt_config.get('alg','RS256')
        self.ttl = jwt_config.get('ttl', default_ttl)


    def encode(self, payload, **kwargs):

        if self.priv_key is None:
            raise Exception('No private key configured for JWT encoding')

        # we insist on an iss - use ours or let caller override
        if payload.get('iss') is None:
            payload['iss'] = self.iss

        if self.ttl:
            time_restrictions = {
                'exp': now(self.ttl),
                'nbf': now(),
                'iat': now()
            }
            payload.update(time_restrictions)
  
        return jwt.encode(payload, key=self.priv_key, algorithm=self.alg, **kwargs)


    def decode(self, token, **kwargs):

        if self.pub_key is None:
            raise Exception('No public key configured for JWT decoding')
        
        if 'issuer' not in kwargs:
            kwargs['issuer'] = self.iss

        return jwt.decode(token, key=self.pub_key, algorithms=[self.alg], **kwargs)


class JwtSym(JwtASym):
    """ Symmetric JWT """

    def __init__(self, jwt_config=None):
        
        self.iss = jwt_config.get('iss')
        self.priv_key = jwt_config.get('key')
        self.pub_key = jwt_config.get('key')
        self.alg = jwt_config.get('alg','HS256')
        self.ttl = jwt_config.get('ttl', default_ttl)


class   JwtEncoder:
    """ Create appropriate encoder. """

    def __init__(self, jwt_config=None):

        if jwt_config is None:
            jwt_config = {
                'key': token_bytes(16),
                'alg' : 'HS256',
                'iss' : None,
            }
            self.jwt = JwtSym(jwt_config=jwt_config)
            
        elif 'key' in jwt_config:
            self.jwt = JwtSym(jwt_config=jwt_config)

        elif 'jwks_url' in jwt_config:
            self.jwt = Jwks(url=jwt_config['jwks_url'])

        elif 'cert' in jwt_config:
            # extract public key from certificate
            cert = load_pem_x509_certificate(jwt_config['cert'])
            
            pubkey = cert.public_key().public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
            jwt_config['pubkey'] = pubkey
            self.jwt = JwtASym(jwt_config)

        elif 'pubkey' in jwt_config or 'privkey' in jwt_config:
            self.jwt = JwtASym(jwt_config=jwt_config)
            
        else:
            raise Exception('No Key config defined')


    def encode(self, *args, **kwargs):

        return self.jwt.encode(*args, **kwargs)


    def decode(self, *args, **kwargs):

        return self.jwt.decode(*args, **kwargs)
    

    def header(self, token):

        return jwt.get_unverified_header(token)
    

    def decode_noverify(self, token):

        return jwt.decode(token, options={'verify_signature': False})
    