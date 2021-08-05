# 변동성이란 가격이 올라가고 내려가는 범위를 말한다. 주가로 치면 주가의 등락폭을 나타내는 거다.
# 래리윌리엄스의 변동성 돌파 전략

import requests
import pandas as pd
from datetime import datetime
import time
import telegram


market_name = 'KRW-BTC'
k = 0.5

def current_price(market_name):     #현재가격정보 갖고 오는 함수
    url = "https://api.upbit.com/v1/ticker"
    querystring = {"markets": market_name}
    headers = {"Accept": "application/json"}
    res = requests.request("GET", url, headers=headers, params=querystring)
    json_data = (res.json())

    market_df = pd.DataFrame(json_data)

    market_df.rename(columns={'market': '종목구분코드', 'trade_date': '최근거래일자(UTC)',
                              'trade_time': '최근거래시각(UTC)', 'trade_date_kst': '최근거래일자(KST)',
                              'trade_time_kst': '최근거래시각(KST)', 'opening_price': '시가',
                              'high_price': '고가', 'low_price': '저가', 'trade_price': '종가',
                              'prev_closing_price': '전일종가', 'change': '보합,상승,하락',
                              'change_price': '변화액의절대값', 'change_rate': '변화율의 절대값',
                              'signed_change_price': '부호가있는변화액',
                              'signed_change_rate': '부호가있는변화율',
                              'trade_volume': '가장최근거래량',
                              'acc_trade_price': '누적거래대금(UTC 0시 기준)',
                              'acc_trade_price_24h': '24시간누적거래대금',
                              'acc_trade_volume': '누적거래량(UTC0시기준)',
                              'acc_trade_volume_24h': '24시간누적거래량',
                              'highest_52_week_price': '52주신고가',
                              'highest_52_week_date': '52주신고가달성일',
                              'lowest_52_week_price': '52주신저가',
                              'lowest_52_week_date': '52주신저가달성일',
                              'timestamp': '타임스탬프'
                              }, inplace=True)

    global 현재가격
    #해당 종목의 현재 시세를 c_price에 저장. 이 아래로 이 함수에서 사용할 결과물 변수를 만들어 나가면 된다.
    현재가격 = json_data[0].get('trade_price')

    return 현재가격
"""
while True:
    now = datetime.now()
    current_price('KRW-BTC')
    print(now.hour,":",now.minute, ":",now.second, "초","현재가격",현재가격)
    time.sleep(1)
"""

def yesterday_status(market_name):
    count_number = '10'  # 시세 캔들 최대 200개까지 요청 가능(count)
    conver_price = "KRW"  # 종가 환산단위 표시 . 생략 가능

    url = "https://api.upbit.com/v1/candles/days"

    querystring = {"market": market_name, "count": count_number, "convertingPriceUnit": conver_price}
    headers = {"Accept": "application/json"}
    res = requests.request("GET", url, headers=headers, params=querystring)

    json_data = (res.json())

    market_df = pd.DataFrame(json_data)

    # 개발가이드를 확인 하면서 컬럼명을 한글로 바꿈
    # converted_trade_price 은 쿼리에서 지정하지 않으면 컬럼이 비어서 출력이 된다. 그리고 한국 마켓의 경우 지정을 해도 none으로 결과값 반환 한다
    market_df.rename(columns={'market': '마켓명',
                              'candle_date_time_utc': 'utc시간',
                              'candle_date_time_kst': 'kst시간',
                              'opening_price': '시가',
                              'high_price': '고가',
                              'low_price': '저가',
                              'trade_price': '종가',
                              'timestamp': '틱저장시간',
                              'candle_acc_trade_price': '누적거래금액',
                              'candle_acc_trade_volume': '누적거래량',
                              'prev_closing_price': '전일종가',
                              'change_price': '전일대비금액',
                              'change_rate': '전일대비변화량',
                              'converted_trade_price': '한화환산금액'

                              }, inplace=True)
    """print(market_df)"""
    yesterday_data = market_df.iloc[1]
    today_data = market_df.iloc[0]
    global 전날종가
    global 전날고가
    global 전날저가
    global 오늘시가

    전날종가 = yesterday_data ['종가']
    전날고가 = yesterday_data ['고가']
    전날저가 = yesterday_data ['저가']
    오늘시가 = today_data ['시가']
    """
    print(yesterday_data)
    print(today_data)
    """

def get_target_price(market_name):
    yesterday_status(market_name)
    global 목표가
    목표가 = 오늘시가 + (전날고가 - 전날저가) * k
    return 목표가

def telegram_bot(message):
    bot = telegram.Bot(token="1916543022:AAGOduTrGMCluQne4Ax_y3NDJrY0_C3atA4")
    chat_id = 718692584
    bot.sendMessage(chat_id=chat_id, text=message) # 메세지 보내기



current_price(market_name)
get_target_price(market_name)

message_content= market_name,현재가격
message_content2= market_name,목표가

i=0
while i<30:
    telegram_bot("현재가격")
    telegram_bot(message_content)
    telegram_bot("목표가격")
    telegram_bot(message_content2)
    i=i+1
    continue


