import requests
import json
import datetime
import time

API_URL = "https://www.alphavantage.co/query"
API_KEY = "CU6GB0TZL1ZURLJY"
TIME_INTERVAL_TIME = 5
TIME_INTERVAL = str(TIME_INTERVAL_TIME) + "min"
FUNCS = ["GLOBAL_QUOTE", "TIME_SERIES_INTRADAY"]
TICKERS = ["EURUSD"]
NUM = []
stocks_bought = {}



class algorithms:
    def __init__(self, ticker):
        self.ticker = ticker

    def basic(self, price, volume, time, prcnt_chng):
        if prcnt_chng > 0.01:
            stocks_bought[self.ticker].buy(time, price, volume)
            print("BUYING value: " + str(float(price) * volume))

        # checking whether to sell them or not

        all_times = list(stocks_bought[self.ticker].holds.keys())
        if len(all_times) >= 1:
            for t in all_times:
                bought_price = stocks_bought[self.ticker].holds[t][0]
                diff = price - bought_price
                chng_since_bought = round(
                    ((diff / bought_price) * 100), 2)
                    # 0.4 or chng_since_bought < -0.98
                if chng_since_bought > 0.5 or chng_since_bought < 0:
                    gain, loss = stocks_bought[self.ticker].sell(t, price)
                    return gain, loss
    # def volume_basic(self, price, cap, time)
    #     return None


class stock:
    def __init__(self, ticker):
        self.ticker = ticker
        # the time volume and price a stock was bought for
        # time : [price, volume, value]
        self.holds = {}

    def buy(self, time, price, volume):
        NUM.append(1)
        print('value: ' + str(price * volume))
        self.holds[time] = [price, volume, price * volume]
        print(self.holds)

    def sell(self, time, price):
        # price = self.holds[time][0]
        gain = 0
        loss = 0
        volume = self.holds[time][1]
        print(volume)
        final_value = self.holds[time][2] - (price * volume)
        del self.holds[time]
        if final_value < 0:
            gain += abs(final_value)
        else:
            loss += final_value
        return gain, loss
        


class actions:
    def __init__(self, data, ticker):
        self.algs = algorithms(ticker)
        self.ticker = ticker
        self.all_dates = sorted(
            list(data["Time Series (" + TIME_INTERVAL + ")"].keys()))
        self.data = data

    def prcnt_change(self):
        if len(self.all_dates) == 1:
            return None

        print(self.all_dates[-1])
        print(self.all_dates[-2])
        price = self.data["Time Series (" + TIME_INTERVAL +
                          ")"][self.all_dates[-1]]["4. close"]
        last_price = self.data["Time Series (" + TIME_INTERVAL +
                               ")"][self.all_dates[-2]]["4. close"]

        print('This is CURRENT price: $' + price)
        print('This is LAST PRICE: $' + last_price)

        diff = float(price) - float(last_price)
        pcnt_change = round(((diff / float(last_price)) * 100), 2)
        print(self.ticker + ' has a percent change of: ' +
              str(pcnt_change) + '% in the last ' + TIME_INTERVAL)
        print(price, last_price, pcnt_change)
        return price, last_price, pcnt_change

    def send_to_alg(self):
        temp = self.prcnt_change()
        if temp:
            price, last_price, prcnt_chng = temp
            volume = 5

            result = self.algs.basic(float(price), volume, self.all_dates[-1], prcnt_chng)
            if result:
                gain, loss = result
                return gain, loss
            return None


class tests:
    def __init__(self):
        pass

    def for_testing_simulator(self):
        total_gain = 0
        total_loss = 0
        for ticker in TICKERS:
            stocks_bought[ticker] = stock(ticker)
            TIMES = 384
            for i in range(1, TIMES):
                data_stuff = data_related()
                new_data = data_stuff.data_input_simulator(ticker, i)
                commands = actions(new_data, ticker)
                # commands.prcnt_change()
                temp = commands.send_to_alg()
                if temp:
                    gain, loss = temp
                    total_gain += gain
                    total_loss += loss
                
                print(str(i) + ' out of ' + str(TIMES))
                print("")
            print(stocks_bought[TICKERS[0]].holds)
            print("total gain: " + str(total_gain))
            print("total loss: " + str(total_loss))
            print("total profit: " + str(total_gain - total_loss))
            print(len(NUM))
            

    def for_testing_real(self):
        for ticker in TICKERS:
            TIMES = 21
            for i in range(1, TIMES):
                t = datetime.datetime.utcnow()
                # waits exactly till the next minute to run
                sleeptime = (TIME_INTERVAL_TIME * 60) - \
                    (t.second + t.microsecond/1000000.0)
                time.sleep(sleeptime)

                data_stuff = data_related()
                data_stuff.get_stock_data()
                all_stock_data = data_stuff.data_file()
                commands = actions(all_stock_data[ticker], ticker)
                commands.prcnt_change()
                print(str(i) + ' out of 20')
                print("")


class data_related:
    def __init__(self):
        self.file_name = 'stock_data.json'

    def get_stock_data(self):
        all_stock_data = self.data_file()
        for ticker in TICKERS:
            data = {"function": FUNCS[1],
                    "symbol": ticker,
                    "interval": TIME_INTERVAL,
                    "outputsize": "full",
                    "datatype": "json",
                    "apikey": API_KEY}
            response = requests.get(API_URL, data)
            data = response.json()
            all_stock_data[ticker] = data
            print('Retrieved ' + ticker)
        self.data_file(all_stock_data)

    def data_file(self, data=None):
        if not data:  # if it is to be read
            raw_data = open(
                self.file_name, 'r')
            data = json.load(raw_data)
            raw_data.close()
            return data
        else:  # if it is write
            json_data = open(
                self.file_name, 'w')
            json_data.write(json.dumps(data, indent=2, sort_keys=True))
            json_data.close()
            return

    def data_input_simulator(self, ticker, data_amount):
        raw_data = open(
            self.file_name, 'r')
        data = json.load(raw_data)
        raw_data.close()
        all_keys = sorted(
            list(data[ticker]["Time Series (" + TIME_INTERVAL + ")"].keys()))
        need_keys = all_keys[0:data_amount]
        to_ret = {"Meta Data": data[ticker]["Meta Data"], "Time Series (" + TIME_INTERVAL + ")": {
            date: data[ticker]["Time Series (" + TIME_INTERVAL + ")"][date] for date in need_keys}}
        # print(to_ret)
        return to_ret

# # for data retrieval
# b = data_related()
# b.get_stock_data()

# for testing
c = tests()
c.for_testing_simulator()


