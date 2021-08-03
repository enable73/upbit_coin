#거래 기준 데이터로 비트코인을 벤치마킹 하기 위해
import requests
import pandas as pd

market_name ='USDT-BTC'
count_number = '10' #시세 캔들 최대 200개까지 요청 가능(count)
conver_price = "KRW" #종가 환산단위 표시 . 생략 가능

url = "https://api.upbit.com/v1/candles/days"

querystring = {"market":market_name,"count": count_number, "convertingPriceUnit" : conver_price }
headers = {"Accept": "application/json"}
res = requests.request("GET", url, headers=headers, params=querystring)

json_data =(res.json())

market_df = pd.DataFrame(json_data)

#개발가이드를 확인 하면서 컬럼명을 한글로 바꿈
#converted_trade_price 은 쿼리에서 지정하지 않으면 컬럼이 비어서 출력이 된다. 그리고 한국 마켓의 경우 지정을 해도 none으로 결과값 반환 한다
market_df.rename(columns= {'market':'마켓명',
                           'candle_date_time_utc':'utc시간',
                           'candle_date_time_kst':'kst시간',
                           'opening_price':'시가',
                           'high_price':'고가',
                           'low_price':'저가',
                           'trade_price':'종가',
                           'timestamp':'틱저장시간',
                           'candle_acc_trade_price':'누적거래금액',
                           'candle_acc_trade_volume':'누적거래량',
                           'prev_closing_price':'전일종가',
                           'change_price':'전일대비금액',
                           'change_rate':'전일대비변화량',
                           'converted_trade_price':'한화환산금액'

                           }, inplace=True)



print(market_df)
