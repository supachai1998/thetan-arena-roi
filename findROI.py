# -*- coding: utf-8 -*-
import webbrowser
import requests
import time
import random
from columnar import columnar
# https://data.thetanarena.com/thetan/v1/hero?id=61924e74c88f1d59ce2430a1
pricebnb = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BNBUSDT").json()
usdtthb = requests.get("https://www.bitkub.com/api/market/information?currency=USDT").json()['data']['last']['thb']

def getPrice(wbnbthc):
    bnbthb = float(pricebnb["price"])*usdtthb
    wbnbthb = bnbthb*wbnbthc
    return wbnbthb


while True:
    try:
        nftID = input("tokenID : ")

        # team mode only
        ROI = 3 # if roi > n%  
        winRateArr , drawRate  = [80,70,60,50,45,40] , 1 #lossRate Automate Calulate
        rateTHCArr = [0.0006,0.00055,0.0005,0.00045,0.0004,0.00035,0.0003,0.00025,0.0002] #wbnb rate

        # ถ้า epic heroRarity=1 
        fetchInfo = "https://data.thetanarena.com/thetan/v1/hero?id="
        baseNFT = "https://marketplace.thetanarena.com/item/"



        rnft = requests.get(fetchInfo+nftID)
        nftInfo = rnft.json()["data"]
        battleCapTHC = nftInfo["heroRanking"]["battleCapTHC"]
        totalBattleCapTHC = nftInfo["heroRanking"]["totalBattleCapTHC"]
        price = nftInfo["sale"]["price"]["value"]/100000000
        name = nftInfo["heroInfo"]["name"]
        rarity = nftInfo["heroInfo"]["rarity"]

        roundDaliy = 8
        baseWin , baseDraw , baseLoss, = 6 , 2 , 1
        bonusWin = 3.25
        if(rarity == 1):
            bonusWin = 6.5
            roundDaliy = 10
        elif (rarity==2):
            bonusWin = 23.55
            roundDaliy = 12
        remain = totalBattleCapTHC - battleCapTHC
        roiday = round(remain/roundDaliy,0)+1
        print()
        print("--------------------------------------------------------------------")
        print("found",name," at ",price,"wbnb","({thb} thb)".format(thb=round(getPrice(price*1.01),2)))
        print("remain play {remain} round".format(remain=remain))
        print("roi {roiday} day".format(roiday=roiday))
        print()
        headers = ["win","THC","price","income","roi%"]
        
        def calTHC(baseWin,baseDraw,baseLoss,bonusWin,totalBattleCapTHC,winRate,drawRate):
            bbWin = baseWin + bonusWin
            remain = totalBattleCapTHC - battleCapTHC
            winTHC = (remain*bbWin)*winRate / 100
            drawTHC = (remain*baseDraw)*drawRate / 100
            lossTHC = (remain*baseLoss)*(winRate - drawRate) / 100
            return winTHC + drawTHC + lossTHC

        def roiCal(rarity,price,battleCapTHC,totalBattleCapTHC):            
            for rateTHC in rateTHCArr:
                print("\t",rateTHC,"wbnb","({thb} thb)".format(thb=round(getPrice(rateTHC),2)))
                data = []
                for winRate in winRateArr:
                    try:
                        totalTHC = calTHC(baseWin,baseDraw,baseLoss,bonusWin,totalBattleCapTHC,winRate,drawRate)
                        income = totalTHC * rateTHC *.96
                        roi = (income - price) / price  * 100
                        strprice = "{price}".format(price=round(price,2))
                        strincome = "{price} (~{pricethb})".format(price=round(income,2),pricethb=round(getPrice(income),2))
                        data.append([winRate,round(totalTHC,2),strprice,strincome,round(roi,2)])
                    except Exception as e:
                        print("NFT not sale")
                        break
                print(columnar(data, headers, no_borders=True))
                print()
        
        roiCal(rarity,price,battleCapTHC,totalBattleCapTHC)
        print("--------------------------------------------------------------------")
        print("ctrl + c to exit")
    except Exception as e:
        print(e)




