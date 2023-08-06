
## JwtEncoder

**JwtEncoder** provides abstracted JWT token generation (using [PyJWT](https://pypi.org/project/PyJWT/) and validation with a dictionary configuration ment to simply creation and deployment.

### Installation

```bash
# pip install JwtEncoder
```
### Usage
> Token creator:
```python
from JwtEncoder import JwtEncoder
from config import jwt_config

jenc = JwtEncoder(jwt_config)

tok = jenc.encode({'hello': 'world', 'aud': 'xyz'})
```
> Token consumer:
```python
from JwtEncoder import JwtEncoder
from config import jwt_config

jenc = JwtEncoder(jwt_config)

payload = jenc.decode(tok, audience='xyz')

print(payload['hello'])  # 'world'

```
#### Signature
```python
jenc = JwtEncoder(jwt_config=config)
```
**`jwt_config`** A python `dict` used to configure a JWT Authorizor.
* The makeup of this dict is discussed below in more detail. 
* By default a symmetric key is generated and tokens are signed using the **HS256** signing algorithm.

#### JwtEncoder Methods

**`tok = jenc.encode(payload, **kwargs)`** 

* Returns a JWT token `tok` from the dict `payload` with a signature and options described in `jwt_config`.  
* Additional options (kwargs) can be included as specified in the [PyJWT documentation](https://pyjwt.readthedocs.io/en/stable/)

**`pay = jenc.decode(tok, **kwargs)`**

* Validates the JWT token `tok` and returns decoded payload `pay` using the signature algorithm, signing keys, and issuer specified in `jwt_config`. 
* Additional options (kwargs) can be provided as specified in [PyJWT documentation](https://pyjwt.readthedocs.io/en/stable/)

**`unverpay = jenc.decode_noverify(tok)`**

* Returns contents of the payload `unverpay`, without verifying the signature or other jwt elements.
* The token should be verified with `jenc.decode()` before any contents are used for authorization or authentication.

**`hdrs = jenc.header(tok)`**
* Returns JWT header options.
* The tok should be validated first with `jenc.decode()`

## *jwt_config* configuration details

**JwtEncoder** uses the **PyJWT** module to implement both encoding and decoding of JWT's. The **`jwt_config`** python *`dict`* permits **JwtEncoder**  to support a various different JWT signing methods. These include:
* shared key signing (symmetric key)
* public and private key (asymmetric key)
* providing an X509 RSA certificate (asymmetric key)
* JWKS url (asymmetric key)

The choice determines which options and which signing algorithms are valid.
#### shared key (symmetric key)

To use a symmetric key **`jwt_config`** is of the form:
```python
jwt_config = {
    'key': 'mysecretkey',
    'alg': 'HS256'  # any valid JWT HS type
    'iss': 'urn:myissuer',
    'ttl': 3600 
}
```
* **`key`** the value of this is the shared binary signing key, and `key` indicates this JwtEncoder will use symmetric key signing.
* **`alg`** specifies the algorithm. For a symmentric key the default signing algorithm is **HS256**.

#### public/private key (asymmetric key)

**`pubkey`** and **`privkey`** (either or both) in **jwt_config*** indicates the JwtEncoder will use asymmetric keys for signing:
```python
jwt_config = {
    'pubkey': b'------BEGIN PUBLIC KEY....',
    'privkey': b'------BEGIN PRIVATE KEY...',
    'alg': 'RS256',
    'iss': 'urn:myissuer'
}
```
* **`pubkey`** and **`privkey`** are binary, PEM encoded keys. 
* Asymmetric signing can include RSA or elliptic curve key pairs (with the appropriate `alg` choice.)
* The default algorithm (`alg`) is **RS256** unless specified otherwise.
* If only the `pubkey` is provided the JwtEncoder can only decode tokens.
* If only the `privkey` is provided the JwtEncoder can only encode tokens.

#### X509 certificate (asymmetric key)
A binary X509 certificate indicates the JwtEncoder will use asymmetric RSA signing keys:
```python
jwt_config = {
    'cert' : b`----BEGIN CERTIFICATE---....',
    'alg': 'RS256',
    'iss': 'urn:xyz'
}
```
* `cert` provides only a public key, and hence  only token decoding - unless a `privkey` is also provided in the `jwt_config`.
* No validation of the X509 certificate authenticity is made.
* The default `alg` is **RS256**

#### JWKS retrieval
Retrieves JASON Web Key Sets (JWKS) signing keys from the specified URL:
```python
jst_config = {
    'jwks_url': 'https://.....',
    'iss': 'api://myapi'
}
```
* This retrieves JWKS keys (for example, from an OIDC provider)  The retrival specifies the algorithms used.
* Any number of keys can be provided by the jwks_url and the decoder will use the algorithm and signing key identifier (`kid`) specified in the jwt header. 
* You can only decode tokens using the `jwks_url` method.

### Additional Options

**`alg`** - *algorithm*

* `alg` specifies the signing algorithm used.
* For symmetric signing the default is `HS256`; for asymmetric signing, `RS256`
* There are various signing algorithms outlined in the JWT specifications, and in the PyJWT documentation.

**`ttl`** - *time to live*

* *time to live* is the length of time the tokens the JwtEncoder generates will be valid.
* If `ttl` is not specified, 3600 Seconds is used by default.
* The token `exp` value is set to the current epoch time + ttl; the token will also include `nbf` and `iat` set to the current time.
* If `ttl` is explicitly set to `None`, the `iat`, `nbf`, and `exp` elements are not added to token encoding - the tokens do not expire.
* Decoding an expired token raises an exception.

**`iss`** - *issuer*

* The issuer is added as `iss` to the payload for encoding tokens, and is verified when tokens are decoded.  
* An alternate issuer can be specified by adding `iss` to the payload before calling `encode({'iss': 'xyz'})`, and can be verified by passing the kwarg `issuer` on decode (e.g. `decode(token,issuer='xyz'))`
* decoding a token where the token `iss` doesn't match the issuer generates an exception.

### Audience Validation

If a jwt has an `aud` (audience) element specified when encoded, then `audience` kwarg must be specified when decoding for the token to validate.
```python
tok = jenc.encode({'aud': 'db21', 'scp': ['table.write']})
...
pay = jenc.decode(tok, audience=['db21', 'db22'])
```
* `audience` can be a `list`, as in the example, containing multiple options.  The token need only match one of them.
* decoding a token without the matching audience generates an exception.

### Generating Signing Keys

For reference only:

Generating Eliptic Curve key pairs using Openssl:
```bash
# openssl ecparam -name prime256v1 -genkey -noout -out private.pem
# openssl ec -in private.pem -pubout -out public.pem
```

Generating RSA key pairs using Openssl:
```bash
# openssl genrsa  -out rsaprivate.pem 2048
# openssl rsa -in rsaprivate.pem -pubout -out rsapublic.pem
```

