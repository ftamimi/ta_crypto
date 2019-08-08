import crypto_3
import talib.abstract
import threading


my_crypto = crypto_3.bittrex_class()
my_crypto.get_currencies()

threads = []

for currency in my_crypto.good_c:
    # print(currency['Currency'])
    if currency['Currency'] == 'BTC':
        currency_string = 'usd-btc'
    else:
        currency_string = 'btc-{}'.format(currency['Currency'])
    # print(currency_string)
    t = threading.Thread(target=my_crypto.above_sma200,
                         args=(currency_string.lower(),))
    t.start()
    threads.append(t)
    # try:
    #
    #     my_crypto.above_sma200(currency_string.lower())
    # except:
    #     print('Nothing returned from {}'.format(currency_string.lower()))

for thread in threads:
    thread.join()




print('The cryptos above the SMA200 are {}'.format(my_crypto.coins_above_sma))


# Currency notices
print('The following cryptos have notices')
for currency in my_crypto.bad_c:

    print('{}:\t{}'.format(currency['CurrencyLong'],currency['Notice'],))

# my_crypto.get_candles('usd-btc')
#
# print(my_crypto.inputs['close'][-1])
# my_crypto.get_current_price('usd-btc')
# print(my_crypto.price)

#
# sma200 = talib.abstract.SMA(my_crypto.inputs, timeperiod=200)
#
# print(sma200[-1])

# MIN MAX

# print('minmax function')
#
# min_vlan, max_val = talib.abstract.MINMAX(my_crypto.inputs, timeperiod=10)
# print(min_vlan,max_val)