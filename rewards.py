import pymongo
import asyncio
import time
import discord
from discord.ext import commands
from discord.ext.commands import Context
from discord import app_commands
from datetime import datetime, timedelta
import time
import random
import tok

MONGO = tok.mongo
client = pymongo.MongoClient(MONGO)
db = client.DiscordJasperBot

# ❔
# ✅
# 🍃
#
def generate_rewards(user_id:int,lootID:str):
    #Put a badge checker
    #Badge Description
    #Some Sytem to make sure you dont see badge twice after claim
    userData = db.UserAdventure.find_one({"_id": user_id})
    catData = db.OnAdventure.find_one({"_id": user_id})
    catData["Total"] += 1
    rewards = []
    if lootID == "Tree":
        catData["GC"] += 1
        ran1 = int(random.randint(1, 10))
        ran2 = int(random.randint(1, 100))
        if ran2 == 69:
            userData["3G"] = True
            rewards.append("Grass Lands Badge 3")
        if ran1 == 10:
            userData["1G"] = True
            userData["Grass"] += 8
            rewards.append("Grass Lands Badge 1")
            rewards.append("8 Grass")
        elif ran1 <= 5:
            userData["Grass"] += 3
            rewards.append("3 Grass")
        elif ran1 <= 8:
            userData["Grass"] += 5
            rewards.append("5 Grass")
            
        #Insert
    elif lootID == "Sand":
        catData["SC"] += 1
        ran1 = int(random.randint(1, 32))
        if ran1 == 32:
            userData["1S"] = True
            userData["Sand"] += 12
            userData["Glass"] += 3
            rewards.append("Desert Dunes Badge 1")
            rewards.append("12 Sand")
            rewards.append("3 Glass")
        elif ran1 <= 31:
            userData["Sand"] += 8
            userData["Glass"] += 2
            rewards.append("2 Glass")
            rewards.append("8 Sand")
        elif ran1 <= 25:
            userData["Sand"] += 5
            userData["Glass"] += 1
            rewards.append("1 Glass")
            rewards.append("5 Sand")
        elif ran1 <= 16:
            userData["Sand"] += 3
            rewards.append("3 Sand")

        #Insert
    elif lootID == "Snow":
        catData["SNC"] += 1
        ran1 = int(random.randint(1, 32))
        if ran1 == 32:
            userData["1SN"] = True
            userData["Snow"] += 8
            userData["Ice"] += 4
            rewards.append("Frost Wastelands Badge 1")
            rewards.append("8 Snow")
            rewards.append("4 Ice")
        elif ran1 <= 31:
            userData["Snow"] += 6
            userData["Ice"] += 3
            rewards.append("3 Ice")
            rewards.append("6 Snow")
        elif ran1 <= 25:
            userData["Snow"] += 4
            userData["Ice"] += 2
            rewards.append("2 Ice")
            rewards.append("4 Snow")
        elif ran1 <= 16:
            userData["Snow"] += 2
            userData["Ice"] += 1
            rewards.append("2 Snow")
            rewards.append("1 Ice")

        #Insert
    elif lootID == "Jungle":
        catData["OC"] += 1
        ran1 = int(random.randint(1, 20))
        if ran1 == 20:
            userData["1O"] = True
            userData["Grass"] += 24
            userData["Wood"] += 8
            userData["Corn"] += 1      
            rewards.append("Orangutan Jungle Badge 1")
            rewards.append("24 Grass")
            rewards.append("8 Wood")
            rewards.append("1 Corn!!(Rare)")
        elif ran1 <= 19:
            userData["Grass"] += 16
            userData["Wood"] += 5
            rewards.append("16 Grass")
            rewards.append("5 Wood")
        elif ran1 <= 15:
            userData["Grass"] += 10
            userData["Wood"] += 3
            rewards.append("10 Grass")
            rewards.append("3 Wood")
        elif ran1 <= 9:
            userData["Grass"] += 6
            userData["Wood"] += 2
            rewards.append("6 Grass")
            rewards.append("2 Wood")

        #Insert
    elif lootID == "Glass":
        catData["GDC"] += 1
        ran1 = int(random.randint(1, 50))
        if ran1 >= 48:
            userData["1GD"] = True
            userData["Sand"] += 24
            userData["Ice"] += 4
            userData["Gem"] += 1      
            rewards.append("Glass Desert Badge 1")
            rewards.append("24 Sand")
            rewards.append("8 Ice")
            rewards.append("1 Gem!!(Rare)")
        elif ran1 == 11:
            userData["3GD"] = True
            userData["Gem"] += 3      
            rewards.append("3 Gems!!! (Super Rare)")     
            rewards.append("Glass Desert Badge 3") 
        elif ran1 <= 47:
            userData["Sand"] += 16
            userData["Glass"] += 8
            #FINISH
            rewards.append("16 Sand")
            rewards.append("8 Glass")
        elif ran1 <= 37:
            userData["Sand"] += 10
            userData["Glass"] += 5
            rewards.append("10 Sand")
            rewards.append("5 Glass")
        elif ran1 <= 20:
            userData["Sand"] += 8
            userData["Glass"] += 4
            rewards.append("8 Sand")
            rewards.append("4 Glass")

        #Insert
    elif lootID == "Ohio":
        catData["OHC"] += 1
        ran1 = int(random.randint(1, 50))
        if ran1 >= 48:
            userData["1OH"] = True
            userData["Wood"] += 20
            userData["Gem"] += 1
            userData["Corn"] += 4
            userData["Kernal"] += 23
            rewards.append("Ohio Badge 1")
            rewards.append("20 Wood")
            rewards.append("23 Kernal")
            rewards.append("4 Corn!(Rare)")
            rewards.append("1 Gem!!(Rare)")
        elif ran1 == 8:
            userData["3OH"] = True
            userData["Corn"] += 6
            userData["Kernal"] += 69
            rewards.append("69 Kernal!(Rare)")
            rewards.append("6 Corn!!! (Super Rare)")     
            rewards.append("Ohio Badge 3") 
        elif ran1 <= 47:
            userData["Wood"] += 14
            userData["Corn"] += 1
            userData["Kernal"] += 16
            rewards.append("16 Kernal")
            rewards.append("14 Wood")
            rewards.append("1 Corn")
        elif ran1 <= 37:
            userData["Wood"] += 10
            userData["Kernal"] += 12
            rewards.append("12 Kernal")
            rewards.append("10 Wood")
        elif ran1 <= 20:
            userData["Wood"] += 6
            userData["Kernal"] += 10
            rewards.append("10 Kernal")
            rewards.append("6 Wood")

    db.RewardHold.insert_one({"_id":user_id,"rewards":rewards})
    rewards.clear()
    db.OnAdventure.replace_one({"_id":user_id}, catData)
    db.UserAdventure.replace_one({"_id": user_id},userData)

def description_Tree(user_id:int)->str:
    userData = db.UserAdventure.find_one({"_id": user_id})
    #True and Flase Will be emojis True(Badge) False(?)
    G1,G2,G3,G4 = "E","E","E","E"
    if userData["1G"] == True:
        G1 = "✅"
    else:
        G1 = "❔"
    if userData["2G"] == True:
        G2 = "✅"
    else:
        G2 = "❔"
    if userData["3G"] == True:
        G3 = "✅"
    else:
        G3 = "❔"
    if userData["4G"] == True:
        G4 = "✅"
    else:
        G4 = "❔"

    Grass = "E"
    if userData["Grass"] > 0:
        Grass = "🍃"
    else:
        Grass = "❔"
    
    des = f"We all start some where and the Grasslands is a perfect starting area with lots of green hills and meadows.\nRisk 0%\nBadges unlocked {G1},{G2},{G3},{G4}\nLoot in area {Grass}"
    return des

def description_Sand(user_id:int)->str:
    userData = db.UserAdventure.find_one({"_id": user_id})
    #True and Flase Will be emojis True(Badge) False(?)
    S1,S2 = "E","E"
    if userData["1S"] == True:
        S1 == "✅"
    else:
        S1 == "❔"
    if userData["2S"] == True:
        S2 == "✅"
    else:
        S2 == "❔"
    Sand,Glass = "E","E"
    if userData["Sand"] > 0:
        Sand = "⏳"
    else:
        Sand = "❔"
    if userData["Glass"] > 0:
        Glass = "🪟"
    else: 
        Glass = "❔"
    des = f"As you venture further you enter the dunes filled with nothing but sand and that one tumbleweed durring a shot-off, Hopefully you will find a dessert temple  \nRisk 0%\nBadges unlocked {S1},{S2}\nLoot in area {Sand},{Glass}"
    return des

def description_Frost(user_id:int)->str:
    userData = db.UserAdventure.find_one({"_id": user_id})
    #True and Flase Will be emojis True(Badge) False(?)
    SN1,SN2 = "E","E"
    if userData["1SN"] == True:
        SN1 == "✅"
    else:
        SN1 == "❔"
    if userData["2SN"] == True:
        SN2 == "✅"
    else:
        SN2 == "❔"
    Snow,Ice = "E","E"
    if userData["Snow"] > 0:
        Snow == "❄️"
    else:
        Snow == "❔"
    if userData["Ice"] > 0:
        Ice = "🧊"
    else: 
        Ice = "❔"
    
    des = f"After you finish crossing the sand dessert you approach a new dessert made out of snow and ice. With blue spruces on a flat wasteland who knows if you will find anything good.\nRisk 0%\nBadges unlocked {SN1},{SN2}\nLoot in area {Snow},{Ice}"
    return des


def description_Jungle(user_id:int)->str:
    userData = db.UserAdventure.find_one({"_id": user_id})
    #True and Flase Will be emojis True(Badge) False(?)
    O1,O2 = "E","E"
    if userData["1O"] == True:
        O1 == "✅"
    else:
        O1 == "❔"
    if userData["2O"] == True:
        O2 == "✅"
    else:
        O2 == "❔"
    Grass,Wood,Corn = "E","E","E"
    if userData["Grass"] > 0:
        Grass == "🍃"
    else:
        Grass == "❔"
    if userData["Wood"] > 0:
        Wood = "🪵"
    else: 
        Wood = "❔"
    if userData["Corn"] > 0:
        Corn = "🌽"
    else: 
        Corn = "❔"
    
    des = f"You enter a forest filled with monkeys idkkk what else to say I am tired\nRisk 5%\nBadges unlocked {O1},{O2}\nLoot in area {Grass},{Wood},{Corn}"
    return des



def description_EnchForest(user_id:int)->str:
    userData = db.UserAdventure.find_one({"_id": user_id})
    #True and Flase Will be emojis True(Badge) False(?)
    O1,O2 = "E","E"
    if userData["1O"] == True:
        O1 == "✅"
    else:
        O1 == "❔"
    if userData["2O"] == True:
        O2 == "✅"
    else:
        O2 == "❔"
    Grass,Wood = "E","E"
    if userData["Grass"] > 0:
        Grass == "🍃"
    else:
        Grass == "❔"
    if userData["Wood"] > 0:
        Wood = "🪵"
    else: 
        Wood = "❔"
    
    des = f"\nRisk 5%\nBadges unlocked {G1},{G2},{G3},{G4}\nLoot in area {Grass}"
    return des



def description_Glass(user_id:int)->str:
    userData = db.UserAdventure.find_one({"_id": user_id})
    GD1,GD2,GD3 = "E","E","E"
    if userData["1GD"] == True:
        GD1 == "✅"
    else:
        GD1 == "❔"
    if userData["2GD"] == True:
        GD2 == "✅"
    else:
        GD2 == "❔"
    if userData["3GD"] == True:
        GD3 == "✅"
    else:
        GD3 == "❔"
    Sand,Ice,Glass,Gem = "E","E","E","E"
    if userData["Sand"] > 0:
        Sand == "⏳"
    else:
        Sand == "❔"
    if userData["Ice"] > 0:
        Ice = "🧊"
    else: 
        Ice = "❔"
    if userData["Glass"] > 0:
        Glass = "🪟"
    else: 
        Glass = "❔"
    if userData["Gem"] > 0:
        Gem = "💎"
    else: 
        Gem = "❔"
    des = f"\nRisk 5%\nBadges unlocked {GD1},{GD2},{GD3}\nLoot in area {Sand},{Glass},{Ice},{Gem}"
    return des

def description_Ohio(user_id:int)->str:
    userData = db.UserAdventure.find_one({"_id": user_id})
    OH1,OH2,OH3 = "E","E","E"
    if userData["1OH"] == True:
        OH1 == "<:amonguspog:886652968051560488>"
    else:
        OH1 == "❔"
    if userData["2OH"] == True:
        OH2 == "<:amonguspog:886652968051560488>"
    else:
        OH2 == "❔"
    if userData["3OH"] == True:
        OH3 == "<:amonguspog:886652968051560488>"
    else:
        OH3 == "❔"
    Wood,Kernal,Gem,Corn = "E","E","E","E"
    if userData["Wood"] > 0:
        Wood = "🪵"
    else:
        Wood == "❔"
    if userData["Kernal"] > 0:
        Kernal = "🍿"
    else: 
        Kernal = "❔"
    if userData["Corn"] > 0:
        Corn = "🌽"
    else: 
        Corn = "❔"
    if userData["Gem"] > 0:
        Gem = "💎"
    else: 
        Gem = "❔"
    des = f"\nRisk 0%\nBadges unlocked {OH1},{OH2},{OH3}\nLoot in area {Kernal},{Wood},{Gem},{Corn}"
    return des