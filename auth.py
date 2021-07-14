# Python 3
## 인증 위한 토큰 생성
import jwt
import uuid

payload = {
    'access_key': '5cgQpQuihmWKVjnXctegMi1nfpeo6JCyX6Ul0EFG',
    'nonce': str(uuid.uuid4()),
}

jwt_token = jwt.encode(payload, 'iz8ELlYocxAQHsknFqUfmVU9o6s4cjGuR5GYJxHU')
authorization_token = 'Bearer {}'.format(jwt_token)

print(authorization_token)