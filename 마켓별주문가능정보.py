import json

import pandas as pd
import jwt
import uuid
import pprint #json출력을 이쁘게 하기 위해
import hashlib
from urllib.parse import urlencode


import requests

access_key = '5cgQpQuihmWKVjnXctegMi1nfpeo6JCyX6Ul0EFG'
secret_key = 'iz8ELlYocxAQHsknFqUfmVU9o6s4cjGuR5GYJxHU'
server_url = 'https://api.upbit.com'
query = {
    'market': 'KRW-ETH',
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

json_data = (res.json())

# json 출력시 이쁘게 보이도록 하기 위해 사용 함
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(json_data)
print("데이터 타입은 ",type(json_data))

#주문 가능 정보

