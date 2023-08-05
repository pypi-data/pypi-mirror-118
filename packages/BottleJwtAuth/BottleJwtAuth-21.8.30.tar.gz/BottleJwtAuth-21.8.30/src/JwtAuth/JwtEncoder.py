from secrets import token_bytes
from cryptography.x509 import load_pem_x509_certificate
from cryptography.hazmat.primitives import serialization
import jwt

from .JWKS import Jwks

class JwtASym:
    """ Asymmetric encoded JWT """
    
    def __init__(self, key_config):
        
        self.iss = key_config.get('iss')
        self.pub_key = key_config.get('pubkey')
        self.priv_key = key_config.get('privkey')
        self.alg = key_config['alg']


    def encode(self, payload, **kwargs):

        headers = {'iss': self.iss}
        if 'headers' in kwargs:
            headers.update(kwargs['headers'])
            del kwargs['headers']

        return jwt.encode(payload, key=self.priv_key, algorithm=self.alg, **kwargs)


    def decode(self, token, **kwargs):
        print('***', kwargs)
        if 'issuer' in kwargs:
            del kwargs['issuer']
        return jwt.decode(token, key=self.pub_key, algorithms=[self.alg], issuer=self.iss, **kwargs)


class JwtCert(JwtASym):
    """ Decode from X509 certificate """

    def __init__(self, certificate):

        if type(certificate) is str:
            certificate = certificate.encode('utf-8')

        cert = load_pem_x509_certificate(certificate)
        pem = cert.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        super().__init__(key_config={
                'pubkey': pem,
                'alg' : 'RS256'
            })


class JwtSym:
    """ Symmetric JWT """

    def __init__(self, key_config=None):
        
        self.iss = key_config.get('iss')
        self.priv_key = key_config.get('key')
        self.pub_key = key_config.get('key')
        self.alg = key_config['alg']


    def encode(self, payload, **kwargs):

        headers = {'iss': self.iss}
        if 'headers' in kwargs:
            headers.update(kwargs['headers'])
            del kwargs['headers']
        return jwt.encode(payload, key=self.priv_key, algorithm=self.alg, headers=headers, **kwargs)


    def decode(self, token, **kwargs ):

        return jwt.decode(token, key=self.pub_key, algorithms=[self.alg], issuer=self.iss, **kwargs)


class   JwtEncoder:
    """ Create appropriate encoder. """

    def __init__(self, key_config=None):

        if key_config is None:
            key_config = {
                'key': token_bytes(),
                'alg' : 'HS256',
                'iss' : None,
            }
            self.jwt = JwtSym(key_config=key_config)
            
        elif 'key' in key_config:
            self.jwt = JwtSym(key_config=key_config)

        elif 'pubkey' in key_config or 'privkey' in key_config:
            self.jwt = JwtASym(key_config=key_config)

        elif 'url' in key_config:
            self.jwt = Jwks(url=key_config['url'])

        elif 'cert' in key_config:
            self.jwt = JwtCert(certificate=key_config['cert'])

        else:
            raise Exception('No Key config defined')


    def encode(self, *args, **kwargs):

        return self.jwt.encode(*args, **kwargs)


    def decode(self, *args, **kwargs):

        return self.jwt.decode(*args, **kwargs)

