#거래 기준 데이터로 비트코인을 벤치마킹 하기 위해
import requests
import pprint
import pandas as pd

market_name ='KRW-BTC'
count_number = '10' #시세 캔들 최대 200개까지 요청 가능(count)
m_unit = '1' #분 단위. 가능한 값 : 1, 3, 5, 15, 10, 30, 60, 240

url = "https://api.upbit.com/v1/candles/minutes/"+m_unit

querystring = {"market":market_name,"count": count_number}
headers = {"Accept": "application/json"}
res = requests.request("GET", url, headers=headers, params=querystring)

json_data =(res.json())

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(json_data)

market_df = pd.DataFrame(json_data)

#개발가이드를 확인 하면서 컬럼명을 한글로 바꿈
market_df.rename(columns= {'market':'마켓명',
                           'candle_date_time_utc':'utc시간',
                           'candle_date_time_kst':'kst시간',
                           'opening_price':'시가',
                           'high_price':'고가',
                           'low_price':'저가',
                           'trade_price':'종가',
                           'timestamp':'틱저장시간',
                           'candle_acc_trade_price':'누적거래금액',
                           'candle_acc_trade_volume':'누적거래량','unit':'분'
                           }, inplace=True)

print(market_df)

#server_url + "/v1/accounts"
