import requests
import json


class Tsunami:

    def __init__(self, dapp, amm, myAddress=None, node='https://nodes.wavesexplorer.com'):
        self.dapp = dapp
        self.amm = amm
        self.myAddress = myAddress
        self.node = node

    node = 'https://nodes.wavesexplorer.com'

    amm = '3P9mFc9Zn9bsk9McUXECybF4imt7691VM1F'  # closePosition
    dapp = '3PJ8HS6FmeM3owQUwv6znVbAzQXFtxNUYDs'  # increasePosition

    address = '3PP6kMgzK2d9zP4i5Zt7RtbpjaMZZzdhR63'

    get_position_str = "getPosition()"

    def getSpotPrice(self):
        spot_price = requests.post(self.node + '/utils/script/evaluate/' + self.amm,
                                   json={"expr": "getSpotPrice()"}).json()
        return spot_price['result']['value']

    def getMarketPrice(self):
        twapSpotPrice = requests.post(self.node + '/utils/script/evaluate/' + self.amm,
                                      json={"expr": "getTwapSpotPrice()"}).json()
        return twapSpotPrice['result']['value']

    def getIndexPrice(self):
        oracle_price = requests.post(self.node + '/utils/script/evaluate/' + self.amm,
                                     json={"expr": "getOraclePrice()"}).json()
        return oracle_price['result']['value']

    def getPosition(self, address):
        position = requests.post(self.node + '/utils/script/evaluate/' + self.amm,
                                 json={"expr": "getPosition(\"" + address + "\")"}).json()
        return position['result']['value']

    def getPositionNotionalAndUnrealizedPnl(self, address, option):
        pnl = requests.post(self.node + '/utils/script/evaluate/' + self.amm, json={
            "expr": "getPositionNotionalAndUnrealizedPnl(\"" + address + "\", " + str(option) + ")"}).json()
        data = pnl['result']
        return { "positionNotional" : data['value']['_1'], "unrealizedPnl" : data['value']['_2']}

    def calcRemainMarginWithFundingPaymentAndRolloverFee(self):
        position = self.getPosition(self.myAddress)
        positionSize = position['_1']['value']
        positionMargin = position['_2']['value']
        positionLstUpdCPF = position['_4']['value']
        positionTimestamp = position['_5']['value']
        unrealizedPnl = self.getPositionNotionalAndUnrealizedPnl(self.myAddress, 1)['unrealizedPnl']

        res = requests.post(self.node + '/utils/script/evaluate/' + self.amm, json = { "expr": "calcRemainMarginWithFundingPaymentAndRolloverFee(" + str(positionSize) + ", "  + str(positionMargin) + ", " + str(positionLstUpdCPF) + ", " + str(positionTimestamp) + ", " + str(unrealizedPnl) + ")" }).json() 
        return res
    
    def getLastMinuteId(self):
        req = requests.get('https://nodes.wavesnodes.com/addresses/data/3P9mFc9Zn9bsk9McUXECybF4imt7691VM1F/k_lastMinuteId').json()
        return req['value']
    
    def getLastMinutePrice(self):
        lastMinuteId = self.getLastMinuteId()
        req = requests.get('https://nodes.wavesnodes.com/addresses/data/3P9mFc9Zn9bsk9McUXECybF4imt7691VM1F/k_twapDataLastPrice_' + str(lastMinuteId)).json()
        print(req)

    def getMarginRatioByOption(self, address, option):
        marginRatio = requests.post(node + '/utils/script/evaluate/' + self.amm, json={
            "expr": "getMarginRatioByOption(\"" + address + "\", " + str(option) + ")"}).json()
        return marginRatio['result']['value']

    def getPositionSize(self, address):
        position = self.getPosition(address)
        return position['_1']['value']

    def getPositionMargin(self, address):
        position = self.getPosition(address)
        return position['_2']['value']

    def pon(self, address):
        position = self.getPosition(address)
        return position['_3']['value']

    def positionLstUpdCPF(self, address):
        position = self.getPosition(address)
        return position['_4']['value']


node = 'https://nodes.wavesexplorer.com'

amm = '3P9mFc9Zn9bsk9McUXECybF4imt7691VM1F'  # closePosition
dapp = '3PJ8HS6FmeM3owQUwv6znVbAzQXFtxNUYDs'  # increasePosition

myAddress = '3PP6kMgzK2d9zP4i5Zt7RtbpjaMZZzdhR63'

tsunami = Tsunami(dapp, amm, myAddress=myAddress, node=node)

last = tsunami.getLastMinuteId()

lastPrice = tsunami.getLastMinutePrice()
marketPrice = tsunami.getMarketPrice()

print(marketPrice)


#              let positionSize = $t07705077174._1
#              let positionMargin = $t07705077174._2
#              let pon = $t07705077174._3
#              let positionLstUpdCPF = $t07705077174._4
#              let positionTimestamp = $t07705077174._5
