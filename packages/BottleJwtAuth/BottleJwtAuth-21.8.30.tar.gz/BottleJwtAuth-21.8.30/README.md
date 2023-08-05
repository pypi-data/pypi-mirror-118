
## bottleJwtAuth - JWT Authentication for Bottle

**bottleJwtAuth** provides JWT Bearer token authentication and authorization for [Bottle web Framework](https://bottlepy.org) web apps.


## Installation

```bash
# pip install bottleJwtAuth
```

### Using bottleJwtAuth
```python
from bottle import Bottle
from JwtAuth import JwtAuth
from config import issuer, audience


app = Bottle()

# Create a restriction on any route with a prefix of '/api/'
aud=JwtAuth(jwt_config={issuer=issuer, audience=audience, url_prefix='/api/')

app.install(aud)

# Basic JWT authentication and validation required to access this view:
@app.route('/api/whoami')
def whoami():
    return ...

# Specific claim requirements to access this view:
@app.route('/api/adduser/<user>', claim={'role':['appadmin', 'usradmin']})
def add_user(user=None):
    ....

# No JWT or any other feature is required to access this route
@app.route('/info)
def info():
    return '....'

if __name__ == '__main__:
    app.run()

```
#### Signature and Parameters

```
auth = JwtAuth(jwt_config=jwt_conf, issuer=issuer, audience=audience, url_prefix='/')
```

**`jwt_config`** A python `dict` used to configure a JWT Authorizor.  Discussed below in more detail. Default: a symmetric HS256 key is generated.

**`issuer`** The issuer URN (generally a URL) used for the JWT `iss` on encode and used to verify on decode.  Default is `None`

**`audience`** The audience URN used for verification of the JWT `aud` on decode.  You will need to add this to the payload on encode operations.

**`url_prefix`** The prefix path component used to match route rules where JwtAuth will impose a JWT requirement and verification.  The default is '/' - the whole app.

### Prefix-based JwtAuth

Any bottle routes that matches the **`url_prefix`** of a JwtAuth plugin will have middleware added to retrieve and verify the JWT bearer token form the HTTP `Authentication` header.
The plugin verifies:
* The request has a valid authentication header with a bearer token.
* The token signature is correct
* The iss field matches the expected issuer
* The aud field matches the expected audience
* The token has not expired.

This applies to all routes and subordinate routes defined, unless the route itself disables the JwtAuth plugin.  This is done with the `skip` config in the bottle route statement.

```python
@app.route('/dontcheckjwt', skip=['/api/'])
```
Note the plugin `name` is identical to the `url_prefix`, in the example, `'/api/'`

Multiple JwtAuth plugins can be added to the same app as long as the `url_prefix` of each plugin do not overlap. 

### Specific route restrictions

Additional requirements can be placed on specific routes:
* you can define a **`scope`** (or **`scp`**) restriction on a given view in the route definition.
* you can define **`claim`** restrictions on a given view in the route definition.
* this only applies to routes with the url_prefix applied.
* **`scope`** and **`claim`** requirements can be combined.

Consider an example with a scope requirement:
```python
auth = JwtAuth(config, issuer='urn:xyz', audience='api:testapi', url_prefix='/api')

# Verify JWT and scope
@app.route('/api/test/3', scp='email')
def test3():
    return 'test3 - JWT verified, and scope of email verified'
```
* if more than one scope is specified, the token must contain all of these.  e.g.
```python
@app.route('/api/test/3/, scp=['email', 'User.write'])
def viewx():
    ...
```

With a claim requirement, multiple claims can be required, and the token much be able to satisfy each claim. 

However, only one matching value per claim is required. For example, for a request to access viewy, the token must contain a claim call `name` that contains either 'bob' or 'alice', and must have the `role` of `appadmin` as well.

```python
@app.route('/api/test/4/', claim={'name': ['bob', 'alice'], 'role':'appadmin'})
def viewy():
    ...
```

## *jwt_config* configuration details

The `jwt_config` option is a dict that can take multiple forms, depending on how **JwtAuth** is deployed. This `dict` is provided to an underlying class **JwtEncoder** that itself uses the **PyJWT** module to implement both encoding and decoding of JWT's - though **bottleJwtAuth** is only concerned with decoding of JWTs.

**JwtEncoder** provides a configuration interface to support a few different JST encryption methods, depending on what your needs are.  These include:
* shared key
* providing a public and private key
* providing an X509 RSA certificate
* JWKS url

#### shared key (symmetric key)

To use a symmetric key **`jwt_config`** is of the form:

```python
jwt_config = {
    'key': 'mysecretkey',
    'alg': 'HS256'  # any valid JWT HS type
    'iss': 'myissuer urn'
}
```

#### public/private key (asymmetric key)

```python
jwt_config = {
    'pubkey': b'------BEGIN PUBLIC KEY....',
    'privkey': b'------BEGIN PRIVATE KEY...',
    'alg': 'RS256',
    'iss': 'my issuer urn'
}
```
Note that if if only `pubkey` is provided the encoder can only decode messages - this is sufficient for the role of **JwtAuth**

#### X509 certificate
```python
jwt_config = {
    'cert' : b`----BEGIN CERTIFICATE---....',
    'alg': 'RS256',
    'iss': 'my issuer urn'
}
```
This supports only token decode.

No validation of the X509 certificate is made - only the public key is retrieved.

#### JWKS retrieval
```python
jst_config = {
    'jwks_url': 'https://.....',
    'iss': 'my issuer urn'
}
This retrieves JWKS keys (generally from an OIDC provider)  The retrival specifies the algorithm used.





