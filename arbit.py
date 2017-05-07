###################Importing modules####################
import requests
import json
import time
########################################################

####################Config Variables####################
minVol = 200 #Minimum volume (In BTC) an exchange should have to be taken into account by this program
exchangedToIgnore = ["hitbtc", "indacoin"]
########################################################

def getCoinNames():
  from poloniex import Poloniex
  api =  Poloniex()
  coinList = []
  coins = api.return24hVolume()
  for market in coins:
    if "BTC_" in market and float(coins[market]["BTC"]) > 200:
      coinList.append(market.replace("BTC_","") + "-btc")
  return coinList

#########Prompt user for what coin to analyse###########
def getPair():
    startTime = time.time()
    input("Base Currency: For BTC, press enter instantly. For USD, press enter after 2 seconds.")
    timeDelta = time.time() - startTime
    baseCurrency = "-btc" if timeDelta < 2 else "-usd"
    print("Base currency: " + baseCurrency[1:].upper())
    pair = input("Coin: ") + baseCurrency
    return pair
########################################################

################Function gets market list###############
def getMarketList(pair):
    output = requests.get("https://api.cryptonator.com/api/full/" + pair)
    markets = json.loads(output.content.decode("utf-8"))["ticker"]["markets"]
    return markets
########################################################

######Function finds lowest and highest exchanges#######
def getLowestHighestMarkets(exchangedToIgnore, minVol, markets):
    lowestMarket = {"price": 10000000000, "volume": 0}
    highestMarket = {"price": 0, "volume": 0}
    for market in markets:
        if market["market"].lower() not in exchangedToIgnore:
            market["price"] = marketPrice = float(market["price"])
            market["volume"] = marketVolume = market["volume"] * market["price"]
            
            if float(marketVolume) >= minVol:
                if marketPrice < lowestMarket["price"]:
                    lowestMarket = market

                if marketPrice > highestMarket["price"]:
                    highestMarket = market
        
    return {"lowestMarket" : lowestMarket, "highestMarket" : highestMarket}
########################################################
            
###############Function calculates stats################
def calcStats(lowestHighestMarkets, pair):
    lowestMarket = lowestHighestMarkets["lowestMarket"]
    highestMarket = lowestHighestMarkets["highestMarket"]
    exchangeUrls = {'yobit' : 'http://yobit.net', 'indacoin' : 'http://indacoin.com', 'kuna' : 'http://en.kuna.com.ua', 'bitstamp' : 'http://bitstamp.net', 'btc-e' : 'http://btc-e.com', 'bittrex' : 'http://bittrex.com', 'cex' : 'http://cex.io', 'http://bleutrade' : 'http://bleutrade.com', 'exmo' : 'http://exmo.com', 'hitbtc' : 'http://hitbtc.com', 'poloniex' : 'http://poloniex.com', 'bitfinex' : 'http://bitfinex.com', 'livecoin' : 'http://livecoin.net', 'c-cex' : 'http://c-cex.com', 'kraken' : 'http://kraken.com'}
    
    baseCurrency = pair[-3:]
    potentialGainPercent = round(highestMarket["price"] / (lowestMarket["price"] / 100) - 100, 3)
    
    lowestExchangeUrl = exchangeUrls[lowestMarket["market"].lower()]
    highestExchangeUrl = exchangeUrls[highestMarket["market"].lower()]
    
    lowestExchange = lowestMarket["market"]
    highestExchange = highestMarket["market"]
    
    lowestPrice = lowestMarket["price"]
    highestPrice = highestMarket["price"]
    
    return {"baseCurrency" : baseCurrency, "potentialGainPercent" : potentialGainPercent, "lowestExchangeUrl" : lowestExchangeUrl, "highestExchangeUrl" : highestExchangeUrl, "lowestPrice" : lowestPrice, "highestPrice" : highestPrice}
########################################################

#####################Run Functions######################
coinStats = []
for coin in getCoinNames():
    markets = getMarketList(coin)
    lowestHighestMarkets = getLowestHighestMarkets(exchangedToIgnore, minVol, markets)
    coinStats.append(calcStats(lowestHighestMarkets, pair))
########################################################

################Alerts user of findings#################
for coin in coinStats.sort(key=lambda x: x["potentialGainPercent"]):
    print("\n")
    print("Buy at " + stats["lowestExchangeUrl"] + " for " + format(stats["lowestPrice"], '.8f') + " " + stats["baseCurrency"].upper())
    print("Sell at " + stats["highestExchangeUrl"] + " for " + format(stats["highestPrice"], '.8f') + " " + stats["baseCurrency"].upper())
    print("Potential gain: " + str(stats["potentialGainPercent"]) + "%")
########################################################
