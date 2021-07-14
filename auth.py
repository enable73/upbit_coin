import jwt   # PyJWT
import uuid

payload = {
    'access_key': '05OfEAYGLaWtUzgM4AVIDCzJw2bkrUoYJmGITiMD',
    'nonce': str(uuid.uuid4()),
}

jwt_token = jwt.encode(payload, 'PlvCTMq4x9R7DgT9swYACDcxqfK9y7ZGYYoK8YvO')
authorization_token = 'Bearer {}'.format(jwt_token)

