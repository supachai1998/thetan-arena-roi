# -*- coding: utf-8 -*-
import webbrowser
import requests
import time
import random
# https://data.thetanarena.com/thetan/v1/hero?id=61924e74c88f1d59ce2430a1
while True:
    try:
        nftID = input("tokenID : ")

        # team mode only
        ROI = 3 # if roi > n%  
        winRateArr , drawRate  = [80,70,60,50,45,40] , 1 #lossRate Automate Calulate
        rateTHCArr = [0.00045,0.0004,0.00035,0.0003,0.00025,0.0002] #wbnb rate

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
        print()
        print("found",name," at ",price,"wbnb")
        print()


        def roiCal(rarity,price,battleCapTHC,totalBattleCapTHC):
            roundDaliy = 8
            baseWin , baseDraw , baseLoss, = 6 , 2 , 1
            bonusWin = 3.25
            if(rarity == 1):
                bonusWin = 6.5
                roundDaliy = 10
            elif (rarity==2):
                bonusWin = 23.55
                roundDaliy = 12
            for rateTHC in rateTHCArr:
                print("\t\t",rateTHC,"wbnb")
                print("win%","\t","price","\t","income","  roi")
                for winRate in winRateArr:
                    try:
                        bbWin = baseWin + bonusWin
                        remain = totalBattleCapTHC - battleCapTHC
                        winTHC = (remain*bbWin)*winRate / 100
                        drawTHC = (remain*baseDraw)*drawRate / 100
                        lossTHC = (remain*baseLoss)*(winRate - drawRate) / 100
                        totalTHC = winTHC + drawTHC + lossTHC

                        income = totalTHC * rateTHC *.96
                        roi = (income - price) / price  * 100
                        roiday = round(remain/roundDaliy,0)+1
                        print(winRate,"\t",round(price,2),"\t",round(income,2),"\t",roi,roiday,"day")
                    except:
                        print("NFT not sale")
                        break
                print()
                print()
        roiCal(rarity,price,battleCapTHC,totalBattleCapTHC)
        print("ctrl + c to exit")
    except Exception as e:
        print(e)




