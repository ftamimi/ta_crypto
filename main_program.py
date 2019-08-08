from data_types import CryptoDef
import os
import time
from bittrex.bittrex import Bittrex, API_V2_0
from termcolor import colored
import csv
from numpy import array
import numpy
from talib.abstract import *
import sys

api_1 = Bittrex(None, None)
api_2 = Bittrex(None, None, api_version=API_V2_0)

watchlist = ["BTC-LSK", "BTC-NEO", "BTC-ETH", "BTC-STRAT", "BTC-XVG", "BTC-STEEM", "BTC-ZEC", "BTC-SC", "BTC-XLM",
             "BTC-LTC", "USD-BTC", "BTC-EMC", "BTC-CLOAK", "BTC-RDD",
             "BTC-XRP", "BTC-ADA", "BTC-XEM", "BTC-DASH", "BTC-ETC", "BTC-WAVES", "BTC-REP", "BTC-OMG",
             "BTC-XMR", "BTC-GRS", "BTC-VTC", "BTC-TUSD",
             "BTC-QTUM", "BTC-SNT", "BTC-ARDR", "BTC-GBYTE", "BTC-TRX",
             "BTC-VEE", "BTC-NBT", "BTC-DOGE", "BTC-EXCL", "BTC-ZCL",
             "BTC-RLC", "BTC-BCPT", "BTC-NXS", "BTC-MUE", "BTC-RCN", "BTC-SRN"]


def main():
    print_header()
    main_questions()

    # daily/hourly csv
    # load csv and analysis


def print_header():
    print "********************************"
    print "            Crypto"
    print "********************************"


def main_questions():
    response = None

    while response != "x":
        print ""
        print "Main Menu"
        print ""
        print "[A]ssets, [F]ocus mode, [C]reate CSV, [L]oad CSV, [B]acktest, [S]top or E[x]it"
        response = raw_input("What is your selection? ")

        response = response.strip().lower()

        if response == 'a':
            check_assets()
        elif response == 'f':
            focus_mode()
        elif response == 'c':
            create_CSV()
        elif response == 'l':
            read_csv()
        elif response == 'b':
            backtest()
        elif response == 's':
            print "Finding stop values"
        elif response == 'x':
            print "Exiting App"
            sys.exit()
            break
        else:
            print "Not a response I understand."


def check_assets():
    asset_path = "holdings"
    print "Starting checks at", time.ctime()

    btc_price = btc()

    if btc_price:
        btc_price = float(btc_price)
        print "Current price in USD ${}".format(btc_price)
    else:
        main_questions()

    total = 0
    stop_percentage = 7

    btc_amount_file = os.path.join(asset_path, 'btc_amount.txt')
    #btc_amount_file = 'btc_amount.txt'
    #asset_amount_file = 'assets.csv'
    asset_amount_file = os.path.join(asset_path, 'assets.csv')

    with open(btc_amount_file, 'r') as fin:
        btc_amount = float(fin.read())

    with open(asset_amount_file, 'r') as csvin:
        reader = csv.reader(csvin)

        for row in reader:
            crypto_name, crypto_code, units, buy_rate = row[0], row[1], float(row[2]), float(row[3])
            last = float(last_crypto_rate(crypto_code))

            print "{} price is {} and ${}. Worth ${}".format(colored(crypto_name, 'yellow'), last,
                                                             "%.2f" % (last * btc_price),
                                                             (colored("%.2f" % (last * btc_price * units), 'yellow')))

            percent_change = last / buy_rate * 100 - 100
            if percent_change > 0:
                print "*** {} up by {}%. {}% stop is {}".format(crypto_name, colored("%.2f" % percent_change, 'green'),
                                                                stop_percentage,
                                                                "%.8f" % (last * (100 - stop_percentage) / 100))
            else:
                print "*** {} down by {}%. {}% stop is {}".format(crypto_name,
                                                                  colored("%.2f" % (-1 * percent_change), 'red'),
                                                                  stop_percentage,
                                                                  "%.8f" % (last * (100 - stop_percentage) / 100))
                # print "***", crypto_name, "down by", colored("%.2f" % (-1 * percent_change), 'red') + "%"

            # add to total
            total += last * btc_price * units
            # print "Total: ${}".format(total)
    print "Bitcoin price is ${}. Worth ${}".format(btc_price, colored("%.2f" % (btc_price * btc_amount), 'yellow'))
    total += btc_price * btc_amount
    print "Total is ${}".format("%.2f" % total)


def btc():
    try:
        btc_tick = api_1.get_ticker("usd-btc")
        btc_Live = btc_tick["result"]
        return btc_Live["Last"]
    except:
        print "Oops, some issue when getting back Bitcoin price"
        return None


def last_crypto_rate(crypto):
    try:
        tick = api_1.get_ticker(crypto)
        live = tick["result"]
        if live["Last"] == None:
            print colored("***Nothing was found for {}, defaulting with 0".format(crypto), 'red')
            live["Last"] = 0
        return live["Last"]
    except:
        print "Oops, couldn't get info for {}".format(crypto)
        main_questions()


def backtest():
    backtest_coin = None
    while backtest_coin != 'x':
        backtest_coin = raw_input("Which coin do you want to backtest? or E[x]it ")

        if backtest_coin.strip() == "x":
            print "Going back to main menu"
            main_questions()
        else:
            if backtest_coin.strip() == "btc":
                bittrex_pre_string = "USD-" + backtest_coin.upper()
            else:
                bittrex_pre_string = "BTC-" + backtest_coin.upper()

            results_list = []

            inputs = get_candles_for_coin(bittrex_pre_string)
            crypto_ta = ta_analysis(inputs)

            trigger_list = []

            triggers = raw_input("How many triggers? ")

            for questions in range(0,int(triggers)):

                indicators_choice = ['cci','rsi','vol_c',
                                     'macdsignal',
                                     'ema21','sma200']

                print "Which indicator do you want to test against?"
                print "1.   CCI"
                print "2.   RSI"
                print "3.   % Volume Change"
                print "4.   MACD Signal"
                print "5.   EMA 21"
                print "6.   SMA 200"
                indicator = raw_input('Enter the number? ')
                #print '{} indicator picked'.format(int(indicator)-1])
                print '{} indicator picked'.format(indicators_choice[int(indicator) - 1])

                if int(indicator) > 4:
                    print 'Comparing against close price'

                    threshold_index = breaks_threshold(inputs['close'],crypto_ta[(indicators_choice[int(indicator) - 1])])
                #macd
                if 5 > int(indicator) > 3:
                    threshold = raw_input("Checking against breaking a number e.g. 0 or (m)acd ")
                    if threshold == 'm':
                        threshold_index = breaks_threshold(crypto_ta['macd'],
                                                           crypto_ta[(indicators_choice[int(indicator) - 1])])
                    else:
                        threshold_index = breaks_threshold(crypto_ta[(indicators_choice[int(indicator) - 1])],
                                                           int(threshold))
                else:

                    threshold = raw_input('Which threshold did it break? ')
                    threshold_index = breaks_threshold(crypto_ta[(indicators_choice[int(indicator) - 1])], int(threshold))

            # initial condition for threshold
            # threshold_index = breaks_threshold(inputs['close'], crypto_ta['middleband'])
            ##threshold_index = breaks_threshold(crypto_ta['cci'], -100)

            # threshold_index = breaks_threshold(crypto_ta['plus_di'], 25)
            # combine more that one threshold list
            # threshold_index = list(set(threshold_index + threshold_index_2))
                print "{} broke at \n{}".format(format(indicators_choice[int(indicator) - 1]),threshold_index)
                trigger_list.append(threshold_index)
            if int(triggers) == 1:

                threshold_index = trigger_list[0]


            elif int(triggers) == 2:
                threshold_index = []
                tolerance = 2
                for index_1 in trigger_list[0]:
                    for index_2 in trigger_list[1]:
                        if (index_1 > index_2 - tolerance) and (index_1 < index_2 + tolerance):
                            threshold_index.append(index_1)
                print "Matching break points are \n{}".format(threshold_index)

            #we have a list of all the times we broke a threshold

            condition_sma200 = False
            condition_ema21 = False
            condition_macd = False

            print "1.   SMA200 - close above SMA200"
            print "2.   EMA21 - close above EMA21"
            print "3.   MACD - MACD above 0"

            conditions = raw_input('Which conditions? seperate with commas ')

            if not conditions:
                print 'No conditions selected'
            elif ',' in conditions:
                conditions = conditions.split(',')

            else:

                temp = int(conditions)
                conditions = []
                conditions.append(temp)

            for condition in conditions:
                if int(condition) == 1:
                    condition_sma200 = True
                elif int(condition) == 2:
                    condition_ema21 = True
                elif int(condition) == 3:
                    condition_macd = True


            stop_percentage = raw_input('Set the percentage for the stop? ')
            stop_percentage = float(stop_percentage)





            # start calc
            for i in threshold_index:
                buy_price = None
                buy_index = i

                print "checking buy index [{}]".format(buy_index)

                # set to True if we don't need to wait for trigger
                trigger_to_buy = False

                # while not trigger_to_buy:
                #   trigger_to_buy, trigger_index = triggered_buy_condition(buy_index, 20, inputs['close'], crypto_ta)

                # print "Buy index {}, checking if higher than ema21 to initiate buy. Close(+1) {} and ema21(+1) {}".format(
                # buy_index, inputs['close'][buy_index + 1], ema21[buy_index + 1])

                # conditions to meet after triggered
                if inputs['close'][buy_index + 1] > inputs['open'][buy_index + 1]:

                    dont_wait = 0
                    buy_it = True

                    while not buy_price:
                        # don't wait forever! this variable drops

                        buy_price, stop_limit = check_to_buy(buy_index, crypto_ta, stop_percentage,inputs['close'],
                                                             inputs['low'],
                                                             inputs['open'], condition_sma200,condition_ema21,
                                                             condition_macd)
                        buy_index += 1
                        dont_wait += 1
                        print 'try times {}'.format(dont_wait)

                        if dont_wait == 3:
                            print 'trying to quit from loop'
                            buy_it = False
                            break

                    if buy_it:

                    # when do i sell?
                        sell_index = buy_index
                        sell_price = None
                        # print "Selling algorithm"

                        while not sell_price:
                            try:

                                sell_price, stop_limit = check_to_sell(sell_index, stop_percentage,inputs['close'], inputs['open'],
                                                                       inputs['low'], stop_limit, crypto_ta['ema5'])
                                sell_index += 1
                            except Exception as e:
                                print "There was an error: {}".format(e)
                                get_average(results_list)
                                backtest()

                        sold(buy_price, sell_price, results_list)
                else:
                    print "[{}] didn't buy this one, condition wasn't met".format(buy_index)

            # print results_list
            get_average(results_list)


def check_to_buy(buy_index, crypto_ta, stop_percentage, close, low, open, condition_sma200,condition_ema21,condition_macd,):
    #print "buy index = {}".format(buy_index)
    # if close is lower than yesterdays - dont buy
    try:
        if close[buy_index] > close[buy_index + 1]:
            print "current close is lower than last one"
            return False, False
    except Exception as e:
        print 'already at end of list {}'.format(e)
    else:
        okay_to_buy = True
        if condition_sma200:
            if close[buy_index] < crypto_ta['sma200'][buy_index]:
                print 'close lower than sma200'
                okay_to_buy = False
            else:
                print 'sma200 okay'
        if condition_ema21:
            if close[buy_index] < crypto_ta['ema21'][buy_index]:
                print 'close lower than ema21'
                okay_to_buy = False
        if condition_macd:
            if crypto_ta['macd'][buy_index] < 0:
                print 'macd is negative'
                okay_to_buy = False
            else:
                print 'macd okay'

        if okay_to_buy:

            stop = set_stop(close[buy_index + 1], low[buy_index], stop_percentage)
            print "buying now for {}, stop at {}".format(close[buy_index + 1], stop)

            return close[buy_index + 1], stop
        else:
            print'not buying!'
            return False, False


def triggered_buy_condition(buy_index, max_steps, close, crypto_ta):
    print "Trigger to buy started at {}".format(buy_index)
    start_time = time.time()
    high = close[buy_index]

    # I need to find the first green candle after drop back down after breakout
    high_found = False  # will reference index of high to be able to start search for low
    low_found = False

    while not high_found:
        high_found, high = save_high(buy_index, close, high)
        buy_index += 1

    low = high

    while not low_found:
        low_found, low = save_low(high_found, close, low)
        buy_index += 1

    print "High {} and low {}found. Returning values....".format(high_found, low_found)
    return True, low_found


def create_CSV():
    list_of_dictionaries = []
    current_dictionary = {}
    csv_start_time = time.time()

    print "Creating CSV"

    for current_crypto in watchlist:
        inputs = get_candles_for_coin(current_crypto)

        if inputs['close'][-1] != "Nan":
            crypto_ta = ta_analysis(inputs)

            c_candle = lambda x: "Green" if inputs['close'][-1] > inputs['open'][-1] else "Red"
            l_candle = lambda x: "Green" if inputs['close'][-2] > inputs['open'][-2] else "Red"

            # write to csv
            current_dictionary = {"Name": current_crypto,
                                  "Close": inputs['close'][-2],
                                  "RSI": crypto_ta['rsi'][-2],
                                  "MACD": crypto_ta['macd'][-2],
                                  "MACD Signal": crypto_ta['macdsignal'][-2],
                                  "MACD Histogram": crypto_ta['macdhist'][-2],
                                  "SMA 50": crypto_ta['sma50'][-2],
                                  "SMA 200": crypto_ta['sma200'][-2],
                                  "EMA 5": crypto_ta['ema5'][-2],
                                  "EMA 21": crypto_ta['ema21'][-2],
                                  "% Change": inputs['close'][-1] / inputs['close'][-2] - 1,
                                  "Chaikin AD Osc Last": crypto_ta['chaikin_ad_osc'][-2],
                                  "Chaikin AD Osc Now": crypto_ta['chaikin_ad_osc'][-1],
                                  "Chaikin AD Last": crypto_ta['chaikin_ad'][-2],
                                  "Chaikin AD Now": crypto_ta['chaikin_ad'][-1],
                                  "Bollinger Band Upperband": crypto_ta['upperband'][-2],
                                  "Bollinger Band Middleband": crypto_ta['middleband'][-2],
                                  "Bollinger Band Lowerband": crypto_ta['lowerband'][-2],
                                  "Bollinger Band Stretch": ((crypto_ta['upperband'][-2] / crypto_ta['lowerband'][
                                      -2]) - 1) * 100,
                                  "This Candle": c_candle(inputs),
                                  "Last Candle": l_candle(inputs),
                                  "Stop": inputs['low'][-2],
                                  "CCI": crypto_ta['cci'][-2],
                                  "ADX": crypto_ta['adx'][-2],
                                  "DI+": crypto_ta['plus_di'][-2],
                                  "DI-": crypto_ta['minus_di'][-2],
                                  "MFI": crypto_ta['mfi'][-2]
                                  }
            list_of_dictionaries.append(current_dictionary)
    print "writing CSV, this took {} secs".format(time.time() - csv_start_time)
    write_to_dict(list_of_dictionaries)


def write_to_dict(dictionary):
    dict_keys = dictionary[0].keys()
    dict_name = str(time.strftime("%Y%m%d") + "dict.csv")

    sorted_dict_keys = ['Name','Close']

    key_index = 0
    for current_key in sorted_dict_keys:
        dict_keys.insert(key_index, dict_keys.pop(dict_keys.index(current_key)))
        key_index += 1

    with open(dict_name, 'wb') as csvfile:
        dict_writer = csv.DictWriter(csvfile, dict_keys)
        dict_writer.writeheader()
        dict_writer.writerows(dictionary)


def save_high(buy_index, close, high):
    if close[buy_index + 1] > close[buy_index]:
        low = close[buy_index + 1]
        return False, low
    else:
        print "High found: {} at {}".format(high, buy_index)
        return buy_index, high


def save_low(low_index, close, low):
    if close[low_index + 1] < close[low_index]:
        low = close[low_index + 1]
        return False, low
    else:
        print "Low found: {}".format(low)
        return low_index, low


def read_csv():
    filelist = []
    selection = None

    for file in os.listdir('.'):
        if file.endswith(".csv"):
            filelist.append(file)
            filelist.sort(key=os.path.getmtime, reverse=True)

    index = 1
    print ""

    if len(filelist) < 5:
        for csvs in filelist:
            print "{}.    {}".format(index, csvs)
            index += 1
    else:
        for csvs in filelist[:5]:
            print "{}.    {}".format(index, csvs)
            index += 1

    # ask user selection
    print ""
    selection = raw_input("Which file are we going to analyse or E[x]it? ")
    selection = int(selection.strip().lower())

    if selection <= len(filelist) and selection >= 1:
        print "{} selected".format(filelist[selection - 1])
        cryptos = load_file(filelist[selection - 1])
        query_data(cryptos)
    elif selection == "x":
        print "Going back to main menu..."
        main_questions()
    else:
        print "Sorry can't accept that selection!"
        read_csv()


def query_data(cryptos):
    cryptos.sort(key=lambda c: c.Change)

    print ""
    print "The top five movers are: "
    for i in range(1, 6):
        print "{} with {}%".format(cryptos[-i].Name, round(cryptos[-i].Change, 2))

    cryptos.sort(key=lambda c: c.Name)

    # low_RSI
    low_RSI = (l for l in cryptos if l.RSI < 30)
    for name in low_RSI:
        print "{} has an RSI of {}".format(name.Name, "%.2f" % name.RSI)

    low_CCI = (l for l in cryptos if l.CCI < -100)
    for name in low_CCI:
        print "{} has an CCI of {}".format(name.Name, "%.2f" % name.CCI)

    # trending_adx = (a for a in cryptos if a.ADX > 25)
    # for name in trending_adx:
    #     if name.DIPlus > 25:
    #         print "{} is trending positive, {} ADX and {} DI+".format(name.Name, round(name.ADX, 1),
    #                                                                   colored(round(name.DIPlus, 1), 'yellow'))
    #
    #     elif name.DIMinus > 25:
    #         print "{} is trending negatively, {} ADX and {} DI-".format(name.Name, round(name.ADX, 1),
    #                                                                     colored(round(name.DIMinus, 1), 'red'))

    chaikin_osc_breaking = (c for c in cryptos if (c.ChaikinADOscLast < 0) and (c.ChaikinADOscNow > 0))
    for name in chaikin_osc_breaking:
        print "{} moved from negative to positive on the Chaikin Oscillator".format(name.Name)

        # breaking_out_bband = (b for b in cryptos if b.BollingerBandUpperband < b.Close)
        # for name in breaking_out_bband:
        #     print "{} is breaking Upper Bollinger Band".format(name.Name)


def load_file(filename):
    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)

        crypto_list = []
        for row in reader:
            c = CryptoDef.create_from_dict(row)
            crypto_list.append(c)

        return crypto_list


def check_to_sell(sell_index,stop_percentage, close, open, low, stop_limit, ema5):
    try:

        if low[sell_index + 1] < stop_limit:
            print "hit stop limit at {}".format(stop_limit)
            sell_price = stop_limit
            return sell_price, stop_limit
        elif close[sell_index + 1] < ema5[sell_index + 1]:
            print "dropped below ema5, close at {}".format(close[sell_index + 1])
            sell_price = close[sell_index + 1]
            return sell_price, stop_limit
        elif close[sell_index + 1] > open[sell_index + 1] and open[sell_index + 1] > open[sell_index] and low[
                    sell_index + 1] > low[sell_index]:
            # print "increasing stop limit from {} to {} as price went up".format(low[sell_index],low[sell_index + 1])
            stop_limit = set_stop(close[sell_index + 1], low[sell_index],stop_percentage)
            return None, stop_limit
        else:
            # print "not selling yet"
            return None, stop_limit

    except Exception as e:
        print "sell index too high: {}".format(e)


def sold(buy_price, sold_price, results_list):
    difference = sold_price / buy_price * 100
    print "Bought at {}, sold at {}. Worth {}%".format(buy_price, sold_price, colored(round(difference, 1), 'yellow'))
    results_list.append(difference)


def set_stop(close, low, stop_percentage):
    stop_percentage = (100 - stop_percentage)/100
    if close * stop_percentage > low:
        stop = close * stop_percentage
    else:
        stop = low

    return stop


def get_average(results_list):
    total = 0
    for num in results_list:
        total += num
    if total:
        average = total / len(results_list)
        print "average is {}%".format(average)
    else:
        print "no results"


def get_candles_for_coin(crypto_coin, time_interval='day'):
    start_time = time.time()

    try:
        open_price = candle_list("O", crypto_coin,time_interval)
        high = candle_list("H", crypto_coin,time_interval)
        low = candle_list("L", crypto_coin,time_interval)
        close = candle_list("C", crypto_coin,time_interval)
        volume = candle_list("V", crypto_coin,time_interval)
        if close is None:
            print 'No results were returned, maybe try a different time interval!!'

        inputs = {
            'open': array(open_price),
            'high': array(high),
            'low': array(low),
            'close': array(close, dtype=numpy.float64),
            'volume': array(volume)
        }


        print "Got candles for {}, completed in {} secs...".format(crypto_coin, round(time.time() - start_time, 1))
        return inputs
    except Exception as e:
        print "There was an error getting the coins: {}".format(e)
        return None


def candle_list(input, x, tick_interval='day'):
    list = []
    try:
        #tick_interval = 'oneMin', 'fifteenMin', 'thirtyMin', 'hour', 'day', 'week'

        # btc_tick = api_2.get_candles(market=x, tick_interval="oneMin")
        # btc_tick = api_2.get_candles(market=x, tick_interval="fifteenMin")
        # btc_tick = api_2.get_candles(market=x, tick_interval="thirtyMin")
        # btc_tick = api_2.get_candles(market=x, tick_interval="hour")
        btc_tick = api_2.get_candles(market=x, tick_interval=tick_interval)
        # btc_tick = api_2.get_candles(market=x, tick_interval="week")

        # print len(btc_tick), "length of BTC tick"
        values = btc_tick["result"]
        for val in values:
            list.append(val[input])
        return list
    except Exception as e:
        #print 'error getting candles: {}'.format(e)
        return None


def vol_change(inputs, timeperiod):


    weights = numpy.repeat(1.0, timeperiod)/timeperiod
    vol = numpy.convolve(inputs['volume'],weights,'valid')


    for n in range(0,timeperiod-1):
        vol = numpy.insert(vol, n, inputs['volume'][n], axis=0)

    #print vol[-5:]

    vol_change_p = (inputs['volume']/vol)*100

    return vol_change_p

def ta_analysis(inputs):
    start_time = time.time()

    rsi = RSI(inputs, timeperiod=14)
    ema5 = EMA(inputs, timeperiod=5)
    ema21 = EMA(inputs, timeperiod=21)
    sma50 = SMA(inputs, timeperiod=50)
    sma200 = SMA(inputs, timeperiod=200)
    cci = CCI(inputs, timeperiod=14)
    macd, macdsignal, macdhist = MACD(inputs, fastperiod=12, slowperiod=26, signalperiod=9)
    adx = ADX(inputs, timeperiod=14)
    plus_di = PLUS_DI(inputs, timeperiod=14)
    minus_di = MINUS_DI(inputs, timeperiod=14)
    upperband, middleband, lowerband = BBANDS(inputs, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
    chaikin_ad_osc = ADOSC(inputs, fastperiod=3, slowperiod=10)
    chaikin_ad = AD(inputs)
    mfi = MFI(inputs, timeperiod=14)
    rocp = ROCP(inputs, timeperiod=10)
    vol_c = vol_change(inputs,timeperiod= 5)

    ta_dict = {
        'rsi': rsi,
        'ema5': ema5,
        'ema21': ema21,
        'sma50': sma50,
        'sma200': sma200,
        'macd': macd,
        'macdsignal': macdsignal,
        'macdhist': macdhist,
        'adx': adx,
        'plus_di': plus_di,
        'minus_di': minus_di,
        'upperband': upperband,
        'middleband': middleband,
        'lowerband': lowerband,
        'chaikin_ad_osc': chaikin_ad_osc,
        'chaikin_ad': chaikin_ad,
        'mfi': mfi,
        'cci': cci,
        'rocp': 100*rocp,
        'vol_c': vol_c # my volume percentage change function
    }

    print "Technical Analysis completed in {} secs...".format(time.time() - start_time)

    return ta_dict




def breaks_threshold(list, threshold):
    #list variable is the technical indicator being fed in
    index_list = []
    below_threshold = None
    index = 0
    if len(list) > 10:
        # print "current index is {}, length of list is {}".format(index, len(list))
        for i in list:
            # print "current index is {}, value in list is {}".format(index, i)
            # add [index] if threshold is a list
            if type(threshold) is int:

                if i < threshold:
                    below_threshold = True
                    index += 1
                else:
                    if below_threshold:
                        index_list.append(index)
                        below_threshold = False
                    index += 1


            elif isinstance(threshold,numpy.ndarray):

                if i < threshold[index]:
                    below_threshold = True
                    index += 1


                else:
                    if below_threshold:
                        index_list.append(index)
                        below_threshold = False
                    index += 1
        return index_list


def breaks_threshold_in_list(list, threshold):
    index_list = []
    below_threshold = None
    index = 0
    if len(list) > 10:
        # print "current index is {}, length of list is {}".format(index, len(list))
        for i in list:
            # print "current index is {}, value in list is {}".format(index, i)
            # add [index] if threshold is a list
            if i < threshold[index]:
                below_threshold = True
                index += 1
            else:
                if below_threshold:
                    index_list.append(index)
                    below_threshold = False
                index += 1
        return index_list


def focus_mode(time_interval='day'):
    focus_coin = None
    focus_input = None
    while focus_coin != 'x':
        #time_interval = 'day'
        print "Current time interval: {}".format(time_interval)
        focus_coin = raw_input("Which coin do you want to focus? change [t]ime interval or E[x]it ")

        if focus_coin.strip() == "x":
            print "Going back to main menu"
            main_questions()
        elif focus_coin.strip() == 't':
            change_time_interval(time_interval)
        else:
            try:

                if focus_coin.strip().lower() == 'btc':
                    bittrex_pre_string = "USD-BTC"
                else:
                    bittrex_pre_string = "BTC-" + focus_coin.upper()

                current_coin = bittrex_pre_string

                inputs = get_candles_for_coin(current_coin, time_interval)
                crypto_ta = ta_analysis(inputs)
            except Exception as e:
                print 'Could not get data back, error: {}'.format(e)
                focus_mode(time_interval)

            print ""

            if not type(inputs['close']) == 'NoneType':
                print "Key points: {} price now, {}% change from (a) {} ago. Last low of {}".format(
                    inputs['close'][-1],
                    round((inputs['close'][-1] / inputs['close'][-2]) * 100 - 100, 2), time_interval,
                    inputs['low'][-2])

                while focus_input != "x":
                    print "c.   Change Coin?"
                    print "1.   Last time a threshold broke?"
                    print "2.   Last few results of an indicator?"
                    print "3.   General output of indicators?"
                    print "4.   Change time interval?"
                    print "5.   Refresh?"
                    print ""
                    focus_input = raw_input("What do you want to check? or E[x]it ")
                    focus_input = focus_input.strip().lower()
                    # if focus_input != "x":
                    #     focus_input = int(focus_input)

                    if focus_input == "x":
                        print "exiting to main menu..."
                        main_questions()
                    elif focus_input == 'c':
                        focus_mode(time_interval)
                    elif focus_input == '1':
                        focus_indicator = raw_input("Which technical indicator? [R]SI, [C]CI, Chaikin [O]scillator ")
                        focus_indicator = focus_indicator.strip().lower()

                        if focus_indicator == "r":
                            focus_threshold = raw_input("What is the threshold? ")
                            focus_threshold = int(focus_threshold.strip().lower())
                            result = breaks_threshold(crypto_ta['rsi'], focus_threshold)
                            days_ago = len(crypto_ta['rsi']) - result[-1] + 1
                            print "RSI broke {} threshold {} days ago".format(focus_threshold, colored(days_ago, 'yellow'))
                        elif focus_indicator == "c":
                            focus_threshold = raw_input("What is the threshold? ")
                            focus_threshold = int(focus_threshold.strip().lower())
                            result = breaks_threshold(crypto_ta['cci'], focus_threshold)
                            days_ago = len(crypto_ta['cci']) - result[-1] + 1
                            print "CCI broke {} threshold {} days ago".format(focus_threshold, colored(days_ago, 'yellow'))
                        elif focus_indicator == "o":
                            focus_threshold = raw_input("What is the threshold? ")
                            focus_threshold = int(focus_threshold.strip().lower())
                            result = breaks_threshold(crypto_ta['chaikin_ad_osc'], focus_threshold)
                            days_ago = len(crypto_ta['chaikin_ad_osc']) - result[-1] + 1
                            print "Chaikin Oscillator broke {} threshold {} days ago".format(focus_threshold,
                                                                                             colored(days_ago, 'yellow'))
                        elif focus_indicator == "ema21":
                            result = breaks_threshold_in_list(inputs['close'], crypto_ta['ema21'])
                            days_ago = len(inputs['close']) - result[-1] + 1
                            print "Close broke ema21 {} days ago".format(colored(days_ago, 'yellow'))
                        elif focus_indicator == "ema5":
                            result = breaks_threshold_in_list(inputs['close'], crypto_ta['ema5'])
                            days_ago = len(inputs['close']) - result[-1] + 1
                            print "Close broke ema5 {} days ago".format(colored(days_ago, 'yellow'))
                        else:
                            focus_mode()

                    elif focus_input == '2':
                        print "2 selected"
                    elif focus_input == '3':
                        print "Showing current levels"
                        print ""
                        print "Close: \t\t{}".format(join_list((inputs['close'][-5:]),'no'))
                        print "ROCP: \t\t{}".format(join_list(crypto_ta['rocp'][-5:],'yes',"%"))
                        print "CCI: \t\t{}".format(join_list((crypto_ta['cci'][-5:]),'yes'))
                        print "RSI: \t\t{}".format(join_list((crypto_ta['rsi'][-5:]),'yes'))
                        print "SMA200: \t{}".format(join_list_and_compare_with_close(crypto_ta['sma200'][-5:],inputs['close'][-5:]))
                        print "Volume: \t{}".format(join_list((inputs['volume'][-5:]),'yes'))
                        rocv = my_ROC(inputs['volume'])
                        print "ROC Vol: \t{}".format(join_list(rocv[-5:],'yes'))
                        print "% Vol: \t\t{}".format(join_list(crypto_ta['vol_c'][-5:],'yes','%'))
                        print ""
                    elif focus_input == '4':
                        change_time_interval(time_interval)
                    elif focus_input == '5':
                        print "refreshing..."
                        inputs = get_candles_for_coin(current_coin, time_interval)
                        crypto_ta = ta_analysis(inputs)

                else:
                    "not a valid response"
            else:
                print 'Nothing returned...'
                focus_mode(time_interval)

def change_time_interval(time_interval):
                        print "Current time interval: {}".format(time_interval)
                        #time_interval = 'day'
                        print " 1. 1 min"
                        print " 2. 15 mins"
                        print " 3. 30 mins"
                        print " 4. 1 hour"
                        print " 5. 1 day"
                        print " 6. 1 week"
                        times = ['oneMin', 'fifteenMin', 'thirtyMin', 'hour', 'day', 'week']
                        time_selection = raw_input("Which time interval? [1-6] ")

                        time_interval = times[int(time_selection)-1]
                        focus_mode(time_interval)


def join_list(our_array, rounded, additional_string=''):
    #print additional_string
    #print type(our_array)
    if type(our_array) is numpy.ndarray:
        array_to_list = our_array.tolist()
    else:
        array_to_list = our_array
    new_list = []


    for each in array_to_list:
        if rounded == 'yes':
            string = "{}{}".format(str(round(each,2)),additional_string)
        else:
            string = "{}{}".format(str(each),additional_string)
        new_list.append(string)


    new_string = ', '.format(additional_string).join(new_list)

    return new_string

def join_list_and_compare_with_close(our_array, close, additional_string=''):

    difference = close - our_array

    array_to_list = difference.tolist()
    new_list = []

    for each in array_to_list:
        string = "{}{} ".format(str(each),additional_string)
        #print each
        new_list.append(string)


    new_string = ', '.join(new_list)

    return new_string

def my_ROC(my_array):
    #my_array = my_array.tolist()
    roc_list = []
    index = 0
    total = len(my_array)
    for each in my_array:
        if index > 0:
            value = ((each - my_array[index-1])/each)*100
        else:
            value = float(0)
        roc_list.append(value)
        index += 1
    return roc_list

if __name__ == '__main__':
    main()


# TODO currency calculator
# TODO add percentage losses or gains in the stop loss functionf
