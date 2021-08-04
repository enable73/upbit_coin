#이동평균 계산을 위해 일일 캔들 조회 api 사용
import requests
import pandas as pd

# 5일 이동 평균 계산 함수
def ma_price(market_name):
    count_number = 10       # 시세 캔들 최대 200개까지 요청 가능(count) 여기서는 5일 이동 평균만 필요하니까 10개 정도가 적당
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
    window = close_price.rolling(5)     # series의 rolling() 메서드 이용해서 5개 즉 5일씩 모든 데이터를 그룹핑한다. 만일 60일 이동 평균을 원한다면 이 숫자를 60으로
    five_day_price = window.mean()      # 그룹핑 한 것끼리만 열에 대한 통계를 낸다. 즉 5개씩 위에서 묶어두었기에 5일간의 종가에 대한 평균이 계산이 된다.
    df_sort['5일이동평균값'] = five_day_price     # 5일 이동 평균 컬럼을 더 해서 새로운 데이터 프레임 셋트를 생성한다.

    """
    print(df_sort)
    """

    global 전날이동평균       #함수 밖에서도 해당 변수를 사용하기 위해 전역 변수 선언
    전날이동평균 = five_day_price[1]      # 일자별로 내림차순으로 정렬이 되어 있어서 인덱스 값이 거꾸로 정렬이 되어 있다. 이 상태에서 전날의 이동평균 최종 값을 구하기 위해 마지막 값(인덱스0)에서 하나 앞의 (인덱스1)의 값을 전날 이동평균 값으로 저장한다.

    return

market_name= "KRW-BTC"
ma_price(market_name)

print(market_name, "의 전날5일이동평균 값=", 전날이동평균)