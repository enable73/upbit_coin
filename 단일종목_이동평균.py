#이동평균 계산을 위해 일일캔들조회 api 사용
import requests
import pandas as pd
from 업비트마켓목록 import market_df

# 5일 이동 평균 계산 함수
def ma_price(market_name):
    count_number = 10  # 시세 캔들 최대 200개까지 요청 가능(count) 이것을 5일 이동 평균
    conver_price = "KRW"  # 종가 환산단위 표시 . 생략 가능

    url = "https://api.upbit.com/v1/candles/days"  # 일별 캔들
    querystring = {"market": market_name, "count": count_number, "convertingPriceUnit": conver_price}
    headers = {"Accept": "application/json"}
    res = requests.request("GET", url, headers=headers, params=querystring)
    json_data = (res.json())

    # 이동평균계산에 필요한 기본 데이터
    market = []
    day_opening_price = []
    day_high_price = []
    day_low_price = []
    day_trade_price = []
    day_volume = []
    date = []

    for i in range(int(count_number)):
        market.append(json_data[i].get('market'))
        day_opening_price.append(json_data[i].get('opening_price'))  # 시가
        day_high_price.append(json_data[i].get('high_price'))  # 고가
        day_low_price.append(json_data[i].get('low_price'))  # 저가
        day_trade_price.append(json_data[i].get('trade_price'))  # 종가
        day_volume.append(json_data[i].get('candle_acc_trade_volume'))  # 누적거래량
        date.append(json_data[i].get('candle_date_time_kst'))  # 한국 시간 기준일자

    new_dic = dict(일자=date,
                   종목=market,
                   시가=day_opening_price,
                   고가=day_high_price,
                   저가=day_low_price,
                   종가=day_trade_price,
                   누적거래량=day_volume)

    df = pd.DataFrame(new_dic)

    close_price = df['종가']
    # series의 rolling() 메서드 이용해서 5개 5일씩 모든 데이터를 그룹핑한다.
    window = close_price.rolling(5)
    # 그룹핑 한 것끼리만 열에 대한 통계를 낸다. 즉 5개씩 위에서 묶어두었기에 5일간의 종가에 대한 평균이 계산이 된다.
    avg_trade_price = window.mean()
    global last_ma5
    last_ma5 = avg_trade_price.index[-2]
    # 현재 종목 가격이 전일의 이동평균보다 높으면 상승장. 그렇지 않으면 하락장으로 판단 한다.
    return

# 현재 가격 갖고 오는 함수
def current_price(market_name):
    url = "https://api.upbit.com/v1/ticker"
    querystring = {"markets": market_name}
    headers = {"Accept": "application/json"}
    res = requests.request("GET", url, headers=headers, params=querystring)
    json_data = (res.json())

    #함수 밖에서도 변수를 사용하기 위해 전역변수로 선언
    global c_price
    #해당 종목의 현재 시세를 c_price에 저장. 이 아래로 이 함수에서 사용할 결과물 변수를 만들어 나가면 된다.
    c_price = json_data[0].get('trade_price')
    return

# 업비트마켓목록 이라는 파일에서 갖고 온 market_df 데이터 프레임에서 ticker 컬럼만 따로 저장
market_data = market_df['ticker']

status = None
for market_name in market_data:
    ma_price(market_name)
    current_price(market_name)
    # 현재 가격과 5일 이동 평균 가격 비교
    if c_price > last_ma5:
        status = "상승장"
        print(market_name,"의 현재 가격:",c_price,"----",status)
    else:
        status = "하락장"
        print(market_name,"의 현재 가격:",c_price,"----",status)

