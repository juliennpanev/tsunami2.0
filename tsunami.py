import requests


class Tsunami:

    def __init__(self, dapp, amm, myAddress=None, node='https://nodes.wavesexplorer.com', xtnId='DG2xFkPdDwKUoBkzGAhQtLpSGzfXLiCYPEzeKH2Ad24p'):
        self.dapp = dapp
        self.amm = amm
        self.myAddress = myAddress
        self.node = node
        self.LONG = 1
        self.SHORT = 2

    def getQuoteAssetReserve(self):
        req = requests.get(
            'http://nodes.wavesnodes.com/addresses/data/3P9mFc9Zn9bsk9McUXECybF4imt7691VM1F/k_qtAstR').json()
        return req['value']

    def getQuoteAssetWeight(self):
        req = requests.get(
            'http://nodes.wavesnodes.com/addresses/data/3P9mFc9Zn9bsk9McUXECybF4imt7691VM1F/k_qtAstW').json()
        return req['value']

    def getBaseAssetReserve(self):
        req = requests.get(
            'http://nodes.wavesnodes.com/addresses/data/3P9mFc9Zn9bsk9McUXECybF4imt7691VM1F/k_bsAstR').json()
        return req['value']

    def getBaseAssetWeight(self):
        req = requests.get(
            'http://nodes.wavesnodes.com/addresses/data/3P9mFc9Zn9bsk9McUXECybF4imt7691VM1F/k_bsAstW').json()
        return req['value']

    def getSpotPrice(self):
        spot_price = requests.post(self.node + '/utils/script/evaluate/' + self.amm,
                                   json={"expr": "getSpotPrice()"}).json()
        return spot_price['result']['value']

    def getPositionAdjustedOpenNotional(self):
        pisitionSize = self.getPositionSize(self.myAddress)
        quoteAssetReserve = self.getQuoteAssetReserve()
        quoteAssetWeight = self.getQuoteAssetWeight()
        baseAssetReserve = self.getBaseAssetReserve()
        baseAssetWeight = self.getBaseAssetWeight()

        adjNotional = requests.post(self.node + '/utils/script/evaluate/' + self.amm, json={"expr": "getPositionAdjustedOpenNotional(" + str(
            pisitionSize) + ", " + str(quoteAssetReserve) + ", " + str(quoteAssetWeight) + ", " + str(baseAssetReserve) + ", " + str(baseAssetWeight) + ")"}).json()
        return adjNotional['result']['value']

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
        return {"positionNotional": data['value']['_1'], "unrealizedPnl": data['value']['_2']}

    def calcRemainMarginWithFundingPaymentAndRolloverFee(self):
        position = self.getPosition(self.myAddress)
        positionSize = position['_1']['value']
        positionMargin = position['_2']['value']
        positionLstUpdCPF = position['_4']['value']
        positionTimestamp = position['_5']['value']
        unrealizedPnl = self.getPositionNotionalAndUnrealizedPnl(self.myAddress, 1)[
            'unrealizedPnl']

        res = requests.post(self.node + '/utils/script/evaluate/' + self.amm, json={"expr": "calcRemainMarginWithFundingPaymentAndRolloverFee(" + str(
            positionSize) + ", " + str(positionMargin) + ", " + str(positionLstUpdCPF) + ", " + str(positionTimestamp) + ", " + str(unrealizedPnl['value']) + ")"}).json()
        return res

    def getLastMinuteId(self):
        req = requests.get(
            'https://nodes.wavesnodes.com/addresses/data/3P9mFc9Zn9bsk9McUXECybF4imt7691VM1F/k_lastMinuteId').json()
        return req['value']

    def getLastMinutePrice(self):
        lastMinuteId = self.getLastMinuteId()
        req = requests.get(
            'https://nodes.wavesnodes.com/addresses/data/3P9mFc9Zn9bsk9McUXECybF4imt7691VM1F/k_twapDataLastPrice_' + str(lastMinuteId)).json()
        return req['value']

    def getMarginRatioByOption(self, address, option):
        marginRatio = requests.post(self.node + '/utils/script/evaluate/' + self.amm, json={
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

    def getMarketPriceFromDapp(self):
        req = requests.post(self.node + '/utils/script/evaluate/' + self.dapp,
                            json={"expr": "getMarketPrice(\"" + self.amm + "\")"}).json()
        return req['result']['value']

    def short(self, wallet,  investment, margin, ref):
        minBaseAssetAmount = (investment * margin) / \
            self.getMarketPriceFromDapp()
        wallet.invokeScript(self.amm, "increasePosition", [{"type": "integer", "value": self.SHORT}, {
            "type": "integer", "value": margin}, {"type": "integer", "value": minBaseAssetAmount}, {"type": "string", "value": ref}],
            [{"amount": investment, "assetId": self.xtnId}])
        
    def long(self, wallet,  investment, margin, ref):
        minBaseAssetAmount = (investment * margin) / \
            self.getMarketPriceFromDapp()
        wallet.invokeScript(self.amm, "increasePosition", [{"type": "integer", "value": self.LONG}, {
            "type": "integer", "value": margin}, {"type": "integer", "value": minBaseAssetAmount}, {"type": "string", "value": ref}],
            [{"amount": investment, "assetId": self.xtnId}])

