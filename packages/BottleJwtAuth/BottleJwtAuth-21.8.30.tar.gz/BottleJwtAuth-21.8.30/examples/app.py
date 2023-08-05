import os
from bottle import Bottle
from JwtAuth import JwtAuth
from config import jwks_uri, issuer, audience

DEBUG = os.environ.get('DEBUG', False)

app = Bottle()

aud=JwtAuth(jwt_config={'jwks_url': jwks_uri}, issuer=issuer, audience=audience, url_prefix='/api/')
app.install(aud)

# Not on prefix path
@app.route('/')
def index():
    return 'Hello jwtAuth'

# Verify JWT: signature, audience, issuer
@app.route('/api/test/1')
def test1():
    return 'test1 - signature, audience & issuer'

# Verify skip - not the plugin name is the prefix path
@app.route('/api/test/2', skip=['/api'])
def test2():
    return 'test2 - skipping plugin'

# Verify JWT and scope
@app.route('/api/test/3', scp='email')
def test3():
    return 'test3 - JWT verified, and scope of email verified'

# multiple scopes required
@app.route('/api/test/4', scp=['email', 'openid'])
def test4():
    return 'test4 - JWT verified, must have both email and openid scope'

# claim of 'groups' with either 'sysadmin' or 'sql'
@app.route('/api/test/5', claim={'groups': ['sysadmin', 'sql']})
def test5():
    return 'test5 - JWT verified, must have either sysadmin or sql in group claim'

@app.route('/api/test/6', scp=['email'], claim={'name': 'bob', 'groups': 'sysadmin'})
def test6():
    return 'test6 - JWT and both scope and claims'


if __name__ == '__main__':
    app.run(port=8001, debug=DEBUG, reloader=DEBUG)

