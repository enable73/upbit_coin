#인증 획득
import jwt   # PyJWT 라이브러리를 설치 해야 함
import uuid

payload = {
    'access_key': '05OfEAYGLaWtUzgM4AVIDCzJw2bkrUoYJmGITiMD',
    'nonce': str(uuid.uuid4()),
}

jwt_token = jwt.encode(payload, 'PlvCTMq4x9R7DgT9swYACDcxqfK9y7ZGYYoK8YvO')
authorization_token = 'Bearer {}'.format(jwt_token)

