import datetime as dt
import requests
import os


# Register an free account at newsapi and store the api key in NEWSAPI_KEY variable as an environment variable before you execute the rest of the steps
# Register a free account at Alphavantage and store the api key in 'ALPHAVANTAGE_KEY' variable as an environment variable before you execute the rest of the steps

newsapi_key=os.environ['NEWSAPI_KEY']
avapi_key=os.environ['ALPHAVANTAGE_KEY']

# -------------------------------- DATETIME UTILS ------------------------------#
def date_to_str(date: dt) -> str:
    month = '0' + str(date.month) if len(str(date.month)) < 2 else str(date.month)
    day = '0' + str(date.day) if len(str(date.day)) < 2 else str(date.day)
    return '-'.join([str(date.year), month, day])


def str_to_date(date_string: str) -> dt:
    arr_int = [int(a) for a in date_string.split('-')]
    year, month, date = arr_int[0], arr_int[1], arr_int[2]
    return dt.date(year, month, date)


# -------------------------------- API UTILITIES --------------------------------- #
# -------------------------------- News Extraction --------------------------------- #

def get_news(company: str, period: 7) -> dict:
    assert (isinstance(period, int))
    url = 'https://newsapi.org/v2/everything'
    params_dict = {
        'q': company,
        'from': date_to_str(dt.datetime.now()),
        'to': date_to_str(dt.datetime.now() - dt.timedelta(period)),
        'apiKey': 'newsapi_key',
        'sortBy': 'latest'
    }
    req = requests.get(url=url, params=params_dict)
    req.raise_for_status()
    response = req.json()
    # print('News JSON')
    # print(response['articles'])
    return response['articles']


# -------------------------------- Stock price Extraction and Analysis --------------------------------- #
def get_stock_price(stock_symbol: str, days: int) -> tuple:
    url = 'https://www.alphavantage.co/query'
    params_dict = {
        'function': 'TIME_SERIES_DAILY_ADJUSTED',
        'symbol': stock_symbol,
        'interval': '5min',
        'apikey': avapi_key}
    res = requests.get(url, params_dict)
    res.raise_for_status()
    results = res.json()
    # print('Stock price JSON')
    # print(results)
    st_time = dt.datetime.now() - dt.timedelta(days=days)
    end_time = dt.datetime.now()
    open_prices = []
    dates = []
    while st_time < end_time:
        str_date = date_to_str(st_time)
        try:
            price = results['Time Series (Daily)'][str_date]['4. close']
            open_prices.append(price)
            dates.append(str_date)
        except KeyError:
            pass
        finally:
            st_time += dt.timedelta(days=1)

    return open_prices, dates


def get_deviation(stock_ticker: str, period: int, dev_thresh: float) -> list:

    results, dates = get_stock_price(stock_ticker, period)
    if not results:
        print('No results')
        return 0
    # print({date: result for date, result in zip(dates, results)})
    first_res, first_date = results[0], dates[0]
    deviation = []
    for price, date in zip(results[1:], dates[1:]):
        curr_date = str_to_date(date)
        first_date = str_to_date(first_date)
        if (curr_date - first_date).days == 1:
            diff = abs((float(price) - float(first_res)) / float(first_res))
            if diff > dev_thresh:
                deviation.append((date, price, diff * 100))
        first_res = price
        first_date = date
    return deviation


def stock_price_assessment(company: str, period=7, deviation=0.1) -> dict:
    assert (isinstance(period, int))
    assert (isinstance(deviation, float))
    discrepany = get_deviation(company, period, deviation)
    if discrepany:
        articles = get_news(company, period)
    else:
        print(f'No deviation in the stock price in {company} above {deviation} in the last {period} days')
        articles = None
    return articles
