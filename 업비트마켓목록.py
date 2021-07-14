import requests
import pprint
import pandas as pd

url = "https://api.upbit.com/v1/market/all"

querystring = {"isDetails":"false"}
headers = {"Accept": "application/json"}
res = requests.request("GET", url, headers=headers, params=querystring)

json_data =(res.json())
"""
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(json_data)
"""
market_df = pd.DataFrame(json_data)

#개발가이드를 확인 하면서 컬럼명을 한글로 바꿈
market_df.rename(columns= {'market':'ticker', 'korean_name':'한글명', 'english_name':'영문명', 'market_warning':'유의종목여부'}, inplace=True)
#시장이름으로 재정렬을 하고 알파벳 내림차순으로 정렬
market_df = market_df.sort_values(by = 'ticker', ascending = False, axis = 0)
#특정 컬럼명 중심으로 정렬 이후 인덱스 리셋
market_df = market_df.reset_index(drop=True)


