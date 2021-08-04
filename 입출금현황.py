import jwt
import uuid
import pprint
import hashlib
from urllib.parse import urlencode

import requests

access_key = 'QgV57XiE2YlrNxiHRFtxf1RovVbagfJSfYx24yN9'
secret_key = 'YKwzdGKl7HBJ6upoxrxqxs6xiDOqIClex1XhF6kR'
server_url = 'https://api.upbit.com'


payload = {
    'access_key': access_key,
    'nonce': str(uuid.uuid4()),
}

jwt_token = jwt.encode(payload, secret_key)
authorize_token = 'Bearer {}'.format(jwt_token)
headers = {"Authorization": authorize_token}

res = requests.get(server_url + "/v1/status/wallet", headers=headers)

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(res.json())
