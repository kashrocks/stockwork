import requests
import json
import datetime
import time

API_URL = "https://www.alphavantage.co/query"
API_KEY = "CU6GB0TZL1ZURLJY"
TIME_INTERVAL_TIME = 1
TIME_INTERVAL = str(TIME_INTERVAL_TIME) + "min"
FUNCS = ["GLOBAL_QUOTE", "TIME_SERIES_INTRADAY"]
TICKERS = ["SNAP"]


def get_prcnt_change(ticker, data):

    # getting current time and date in certain format
    c_time = datetime.datetime.now()

    # c_time = c_time - datetime.timedelta(minutes=c_time.minute % TIME_INTERVAL_TIME)
    # c_time = c_time.replace(second=0)

    # comment  when not testing #########################
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
        rec_price = data["Time Series (" + TIME_INTERVAL +
                         ")"][all_keys[-1]]["4. close"]
    else:
        print("Current time: " + c_time_text)
        rec_price = data["Time Series (" + TIME_INTERVAL +
                         ")"][c_time_text]["4. close"]
    last_price = data["Time Series (" + TIME_INTERVAL +
                      ")"][l_time_text]["4. close"]

    print('This is rec_price: ' + rec_price)
    print('This is last_price: ' + last_price)

    diff = float(rec_price) - float(last_price)
    prcnt_change = round(((diff / float(last_price)) * 100), 2)
    print(ticker + ' has a percent change of: ' +
          str(prcnt_change) + '% in the last ' + TIME_INTERVAL)
    print("")


def get_prcnt_change_new(ticker, data):
    all_keys = sorted(
        list(data["Time Series (" + TIME_INTERVAL + ")"].keys()))
    if len(all_keys) == 1:
        return

    print(all_keys[-1])
    print(all_keys[-2])
    rec_price = data["Time Series (" + TIME_INTERVAL +
                     ")"][all_keys[-1]]["4. close"]
    last_price = data["Time Series (" + TIME_INTERVAL +
                      ")"][all_keys[-2]]["4. close"]

    print("Current time: " + all_keys[-1])
    print('This is CURRENT price: $' + rec_price)
    print('This is LAST PRICE: $' + last_price)

    diff = float(rec_price) - float(last_price)
    prcnt_change = round(((diff / float(last_price)) * 100), 2)
    print(ticker + ' has a percent change of: ' +
          str(prcnt_change) + '% in the last ' + TIME_INTERVAL)


def for_testing_simulator():
    # all_stock_data = data_file()
    for ticker in TICKERS:
        # get_prcnt_change(ticker, all_stock_data[ticker])
        TIMES = 50
        for time in range(1, TIMES):
            new_data = data_input_simulator(ticker, time)
            get_prcnt_change_new(ticker, new_data)


def for_testing_real():
    for ticker in TICKERS:
        TIMES = 21
        for i in range(1, TIMES):
            t = datetime.datetime.utcnow()
            # waits exactly till the next minute to run
            sleeptime = (TIME_INTERVAL_TIME * 60) - \
                (t.second + t.microsecond/1000000.0)
            time.sleep(sleeptime)

            get_stock_data()
            all_stock_data = data_file()
            get_prcnt_change_new(ticker, all_stock_data[ticker])
            print(str(i) + ' out of 20')
            print("")


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
            'json_data.json', 'r')
        data = json.load(raw_data)
        raw_data.close()
        return data
    else:  # if it is write
        json_data = open(
            'json_data.json', 'w')
        json_data.write(json.dumps(data, indent=2, sort_keys=True))
        json_data.close()
        return


def data_input_simulator(ticker, data_amount):
    raw_data = open(
        'json_data.json', 'r')
    data = json.load(raw_data)
    raw_data.close()
    all_keys = sorted(
        list(data[ticker]["Time Series (" + TIME_INTERVAL + ")"].keys()))
    need_keys = all_keys[0:data_amount]
    to_ret = {"Meta Data": data[ticker]["Meta Data"], "Time Series (" + TIME_INTERVAL + ")": {
        date: data[ticker]["Time Series (" + TIME_INTERVAL + ")"][date] for date in need_keys}}
    # print(to_ret)
    return to_ret


# for min in range(5):
#     get_stock_data()
#     for_testing()
#     time.sleep(61)

# get_stock_data()
for_testing_real()
