
import jwt   # PyJWT 라이브러리를 설치 해야 함
import uuid

payload = {
    'access_key': 'QgV57XiE2YlrNxiHRFtxf1RovVbagfJSfYx24yN9',
    'nonce': str(uuid.uuid4()),
}

jwt_token = jwt.encode(payload, 'YKwzdGKl7HBJ6upoxrxqxs6xiDOqIClex1XhF6kR')
authorization_token = 'Bearer {}'.format(jwt_token)
