class CryptoDef:
    def __init__(self, Name, Close, RSI, MACD, MACDsignal, MACDhist, SMA50, SMA200, EMA5, EMA21, Change,
                 ChaikinADOscLast, ChaikinADOscNow, ChaikinADLast, ChaikinADNow, BollingerBandUpperband,
                 BollingerBandMiddleband,BollingerBandLowerband,
                 BollingerBandStretch, ThisCandle, LastCandle, Stop, CCI, ADX, DIPlus, DIMinus, MFI,ROCP,
                 vol_c):
        self.Name = Name
        self.Close = Close
        self.RSI = RSI
        self.MACD = MACD
        self.MACDsignal = MACDsignal
        self.MACDhist = MACDhist
        self.SMA50 = SMA50
        self.SMA200 = SMA200
        self.EMA5 = EMA5
        self.EMA21 = EMA21
        self.Change = Change
        self.ChaikinADOscLast = ChaikinADOscLast
        self.ChaikinADOscNow = ChaikinADOscNow
        self.ChaikinADLast = ChaikinADLast
        self.ChaikinADNow = ChaikinADNow
        self.BollingerBandUpperband = BollingerBandUpperband
        self.BollingerBandMiddleband = BollingerBandMiddleband
        self.BollingerBandLowerband = BollingerBandLowerband
        self.BollingerBandStretch = BollingerBandStretch
        self.ThisCandle = ThisCandle
        self.LastCandle = LastCandle
        self.Stop = Stop
        self.CCI = CCI
        self.ADX = ADX
        self.DIPlus = DIPlus
        self.DIMinus = DIMinus
        self.MFI = MFI
        self.ROCP = ROCP
        self.vol_c = vol_c

    @staticmethod
    def create_from_dict(lookup):
        return CryptoDef(
            lookup['Name'],
            float(lookup['Close']),
            float(lookup['RSI']),
            float(lookup['MACD']),
            float(lookup['MACD Signal']),
            float(lookup['MACD Histogram']),
            float(lookup['SMA 50']),
            float(lookup['SMA 200']),
            float(lookup['EMA 5']),
            float(lookup['EMA 21']),
            100*float(lookup['% Change']),
            float(lookup['Chaikin AD Osc Last']),
            float(lookup['Chaikin AD Osc Now']),
            float(lookup['Chaikin AD Last']),
            float(lookup['Chaikin AD Now']),
            float(lookup['Bollinger Band Upperband']),
            float(lookup['Bollinger Band Middleband']),
            float(lookup['Bollinger Band Lowerband']),
            float(lookup['Bollinger Band Stretch']),
            lookup['This Candle'],
            lookup['Last Candle'],
            float(lookup['Stop']),
            float(lookup['CCI']),
            float(lookup['ADX']),
            float(lookup['DI+']),
            float(lookup['DI-']),
            float(lookup['MFI']),
            float(lookup['ROCP']),
            float(lookup['vol_c']),
        )
