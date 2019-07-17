import requests
import json
import datetime
import time

API_URL = "https://www.alphavantage.co/query"
API_KEY = "CU6GB0TZL1ZURLJY"
TIME_INTERVAL_TIME = 1
TIME_INTERVAL = str(TIME_INTERVAL_TIME) + "min"
FUNCS = ["GLOBAL_QUOTE", "TIME_SERIES_INTRADAY"]
TICKERS = ["GOOGL", "SNAP", "BYND"]


def get_prcnt_change(ticker, data):
    
    # getting current time and date in certain format
    c_time = datetime.datetime.now()

    # c_time = c_time - datetime.timedelta(minutes=c_time.minute % TIME_INTERVAL_TIME)
    # c_time = c_time.replace(second=0)

    # replace when not testing #########################
    c_time = c_time.replace(hour=16, minute=0, second=0)

    # dont change the below
    c_time_text = c_time.strftime("%Y-%m-%d %H:%M:%S")

    # getting current time and date in certain format - TIME_INTERVAL_TIME mins
    l_time = c_time - datetime.timedelta(minutes=TIME_INTERVAL_TIME)
    l_time_text = l_time.strftime("%Y-%m-%d %H:%M:%S")

    # getting current price and last price
    all_keys = list(data["Time Series (" + TIME_INTERVAL + ")"].keys())
    if c_time_text not in all_keys:
        print("Current time: " + all_keys[-1])
        rec_price = data["Time Series (" + TIME_INTERVAL + ")"][all_keys[-1]]["4. close"]
    else:
        print('DELETE THIS AFTER')
        print("Current time: " + c_time_text)
        rec_price = data["Time Series (" + TIME_INTERVAL + ")"][c_time_text]["4. close"]
    last_price = data["Time Series (" + TIME_INTERVAL + ")"][l_time_text]["4. close"]

    print('This is rec_price: ' + rec_price)
    print('This is last_price: ' + last_price)

    prcnt_change = round(((1 - float(rec_price) / float(last_price)) * 100), 2)
    print(ticker + ' has a percent change of: ' + str(prcnt_change) + '% in the last ' + TIME_INTERVAL)
    print("")


def for_testing():
    all_stock_data = data_file()
    for ticker in TICKERS:
        get_prcnt_change(ticker, all_stock_data[ticker])


def get_stock_data():
    all_stock_data = data_file()
    for ticker in TICKERS:
        data = {"function": FUNCS[1],
                "symbol": ticker,
                "interval": TIME_INTERVAL,
                "datatype": "json",
                "apikey": API_KEY}
        response = requests.get(API_URL, data)
        data = response.json()
        all_stock_data[ticker] = data
        print('Retrieved ' + ticker)
    data_file(all_stock_data)


def data_file(data=None):
    if not data:  # if it is to be read
        raw_data = open(
            '/home/solink/Git_Repo/My_projects/web_scrape/json_data.json', 'r')
        data = json.load(raw_data)
        raw_data.close()
        return data
    else:  # if it is write
        json_data = open(
            '/home/solink/Git_Repo/My_projects/web_scrape/json_data.json', 'w')
        json_data.write(json.dumps(data, indent=2, sort_keys=True))
        json_data.close()
        return


# for min in range(5):
#     get_stock_data()
#     for_testing()
#     time.sleep(61)

#get_stock_data()
for_testing()
