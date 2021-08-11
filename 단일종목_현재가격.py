import requests
import pprint
import pandas as pd

def current_price(market_name):
    url = "https://api.upbit.com/v1/ticker"
    querystring = {"markets": market_name}
    headers = {"Accept": "application/json"}
    res = requests.request("GET", url, headers=headers, params=querystring)
    json_data = (res.json())

    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(json_data)

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

    """
    print(market_df)
    """
    return

market_name= "KRW-BTC"
current_price(market_name)

print(market_name, "의 현재가격=", 현재가격)





