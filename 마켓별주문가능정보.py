import jwt
import uuid
import hashlib
from urllib.parse import urlencode
import pprint

import requests

access_key = 'QgV57XiE2YlrNxiHRFtxf1RovVbagfJSfYx24yN9'
secret_key = 'YKwzdGKl7HBJ6upoxrxqxs6xiDOqIClex1XhF6kR'
server_url = 'https://api.upbit.com'

query = {
    'market': 'KRW-ETH'
}
query_string = urlencode(query).encode()

m = hashlib.sha512()
m.update(query_string)
query_hash = m.hexdigest()

payload = {
    'access_key': access_key,
    'nonce': str(uuid.uuid4()),
    'query_hash': query_hash,
    'query_hash_alg': 'SHA512',
}

jwt_token = jwt.encode(payload, secret_key)
authorize_token = 'Bearer {}'.format(jwt_token)
headers = {"Authorization": authorize_token}

res = requests.get(server_url + "/v1/orders/chance", params=query, headers=headers)

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(res.json())