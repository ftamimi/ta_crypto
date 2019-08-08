import bittrex
import talib.abstract
import numpy


class bittrex_class:
    def __init__(self):
        self.api_v1 = bittrex.bittrex.Bittrex(None, None)
        self.api_v2 = bittrex.bittrex.Bittrex(None, None, api_version='v2.0')

        self.bad_c = []
        self.good_c = []

    def get_candles(self, coin, interval='day'):
        candles = self.api_v2.get_candles(coin, interval)
        self.candles = candles['result']

        # list comprehension
        open_price = [x['O'] for x in self.candles]
        high = [x['H'] for x in self.candles]
        low = [x['L'] for x in self.candles]
        close = [x['C'] for x in self.candles]
        volume = [x['V'] for x in self.candles]

        self.inputs = {
            'open': numpy.array(open_price),
            'high': numpy.array(high),
            'low': numpy.array(low),
            'close': numpy.array(close, dtype=numpy.float64),
            'volume': numpy.array(volume),
        }

    def get_current_price(self, coin):

        price = self.api_v1.get_ticker(coin)
        self.price = price['result']['Last']

    def get_currencies(self):
        currencies = self.api_v2.get_currencies()
        currencies = currencies['result']

        for currency in currencies:
            if currency['Notice'] != None:
                bad_c = {}
                # print('{}:\t{}\n\t{}'.format(currency['Currency'], currency['CurrencyLong'], currency['Notice']))
                bad_c['Currency'] = currency['Currency']
                bad_c['CurrencyLong'] = currency['CurrencyLong']
                bad_c['Notice'] = currency['Notice']
                self.bad_c.append(bad_c)
            else:
                good_c = {}
                # print(currency)
                good_c['Currency'] = currency['Currency']
                good_c['CurrencyLong'] = currency['CurrencyLong']
                self.good_c.append(good_c)
        # good_c = {}
        # # print(currency)
        # good_c['Currency'] = 'usd-btc'
        # good_c['CurrencyLong'] = 'Bitcoin'
        # self.good_c.append(good_c)

    def above_sma200(self,coin):
        self.coins_above_sma = []
        try:
            self.get_candles(coin)
            sma200 = talib.abstract.SMA(self.inputs, timeperiod=200)

            # print('Current price {}, sma200 {}'.format(self.inputs['close'][-1], sma200[-1]))
            if self.inputs['close'][-1] > sma200[-1]:
                print('{} is above SMA200!!!!'.format(coin))
                self.coins_above_sma.append(coin)
        except:
            pass

