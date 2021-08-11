#비트코인을 기준으로 삼는다
#보통 주식의 경우 20일을 평균적으로 사용하나 코인의 경우 변동성이 심하기에 좀더 짧은 것을 사용해보자
#매수 : 10일 이동평균종가 보다 높을 경우
#매도 : 10일간의 종가중에 가장 낮은 금액 보다 오늘의 종가가 낮을 경우 보유하고 있는 종목 전체 매도

import requests
import pandas as pd
import time
market_name = 'KRW-BTC' #한화로 거래 되는 비트코인을 마켓타이밍 계산을 위한 레퍼런스 종목으로 한다.

def current_price(market_name):
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

def ma_and_low_price(market_name):
    count_number = 20       # 시세 캔들 최대 200개까지 요청 가능(count) 여기서는 10일 이동 평균만 필요하니까 20개 정도가 적당
    conver_price = "KRW"    # 종가 환산단위 표시 . 생략 가능

    # 일별 캔들 조회위한 api
    url = "https://api.upbit.com/v1/candles/days"
    querystring = {"market": market_name, "count": count_number, "convertingPriceUnit": conver_price}
    headers = {"Accept": "application/json"}
    res = requests.request("GET", url, headers=headers, params=querystring)
    json_data = (res.json())

    # 이동평균계산에 필요한 기본 데이터 생성
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
    df_sort = df.sort_values(by=["일자"], ascending=[True])       # 일자를 기준으로 내림차순으로 정렬을 한다. 이유는 최근 일자가 맨 밑으로 정렬하고 5개씩 통계를 내기 위해

    close_price = df_sort['종가']
    window = close_price.rolling(10)     # series의 rolling() 메서드 이용해서 10개 즉 10일씩 모든 데이터를 그룹핑한다. 만일 60일 이동 평균을 원한다면 이 숫자를 60으로
    ten_day_price = window.mean()        # 그룹핑 한 것끼리안에서의 평균값을 찾는다. 즉 10개씩 위에서 묶어두었기에 10일간의 종가에 대한 평균이 계산이 된다.
    low_day_price = window.min()         # 그룹핑 한 것끼리 안에서의 최소값을 찾는다. 즉 10개씩 위에서 묶어두었기에 10일간의 종가중 최소값이 저장 된다.

    df_sort['10일이동평균값'] = ten_day_price     # 10일 이동 평균 컬럼을 더 해서 새로운 데이터 프레임 셋트를 생성한다.
    df_sort['10일중최저종가'] = low_day_price     # 10일 종가중 최저가를 계산해서 컬럼을 더 해서 새로운 데이터 프레임 셋트를 생성한다.
    """
    print(df_sort)
    df_sort.to_excel('sort.xlsx')
    """
    global 전날십일이동평균       # 함수 밖에서도 해당 변수를 사용하기 위해 전역 변수 선언
    global 십일중최저종가     # 함수 밖에서도 해당 변수를 사용하기 위해 전역 변수 선언

    전날십일이동평균 = ten_day_price[1]
    십일중최저종가 = low_day_price[0]

    return 전날십일이동평균,십일중최저종가

while True:
    ma_and_low_price(market_name)
    current_price(market_name)

    if 현재가격 > 전날십일이동평균:
        market_timing = True
        print("오늘 매수 거래 해도 된다")
    else:
        market_timing = False
        print("오늘 매수 거래 하지마")

    if 현재가격 < 십일중최저종가:
        market_signal = False
        print("지금 당장 갖고 있는 종목 싹 다팔아")
    else:
        market_signal = True
        print("지금 현재 마켓타이밍 괜찮아")

    time.sleep(5)

    continue
