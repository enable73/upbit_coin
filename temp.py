import requests
import pandas as pd
market_name = 'KRW-BTC' #한화로 거래 되는 비트코인을 마켓타이밍 계산을 위한 레퍼런스 종목으로 한다.

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

    return

ma_and_low_price(market_name)
print(전날십일이동평균, 십일중최저종가)