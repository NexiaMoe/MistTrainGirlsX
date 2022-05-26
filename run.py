from datetime import datetime
import json
from pprint import pprint
from fastapi import FastAPI, HTTPException, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from typing import Union
import random
import string
import jwt
import psycopg2
from psycopg2.extras import RealDictCursor
conn = psycopg2.connect("dbname=mist user=postgres password=ajipriy0123")
cur = conn.cursor(cursor_factory=RealDictCursor)


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def systime():
    now = datetime.today()
    return now.strftime("%Y-%m-%dT%H:%M:%S")

getMyPref = {}

def getPref(userid):
    cur.execute(f"select * from public.userpref where userid = {int(userid)}")
    
    try:
        sql = json.dumps(cur.fetchone())
        sql = json.loads(sql)
    except:
        sql = None
    
    if sql == None :
        cur.execute(f"""select * from users where "Id" = {int(userid)}""")
        username = json.dumps(cur.fetchone())
        username = json.loads(username)
        
        cur.execute(f"""INSERT INTO public.userpref(userid, "Name", "DateOfBirth", "LocateType", "WeaponLimit", "ArmorLimit", "AccessoryLimit", "AbilityStoneLimit", "SoundMute", "BgmVolume", "SeVolume", "VoiceVolume", "CharacterAutoLockRarity", "MCharacterId1", "MCharacterId2", "MCharacterId3", "MCharacterId4", "MCharacterId5", "IsHomeCharacterRandom", "CurrentHomeViewTypeIsCharacter", "MFieldSkillId1", "MFieldSkillId2", "MFieldSkillId3", "IsHomeFieldSkillRandom", "KnuckleWeaponLevel", "KnuckleWeaponTotalPoint", "SwordWeaponLevel", "SwordWeaponTotalPoint", "AxWeaponLevel", "AxWeaponTotalPoint", "SpearWeaponLevel", "SpearWeaponTotalPoint", "WhipWeaponLevel", "WhipWeaponTotalPoint", "MagicWeaponLevel", "MagicWeaponTotalPoint", "BowWeaponLevel", "BowWeaponTotalPoint", "RodWeaponLevel", "RodWeaponTotalPoint", "GunWeaponLevel", "GunWeaponTotalPoint", "UPartyId", "MQuestId", "BattleAutoSetting", "BattleSpeed", "AutoSellEquipRarity", "AutoSellEquipEvolution", "AutoSellEquipLevel", "AutoSellAbility", "AutoSellSlot", "AdventureTextFeed", "SpecialSkillAnimation", "CurrentClearChapter", "UnlockFeatureFlag", "UnlockEffectFlag", "FunctionHelpFlag", "FunctionHelpFlag2", "TutorialStatus", "BattleAutoSellEquipType", "BattleRaritySellTypeB", "BattleRaritySellTypeA", "BattleRaritySellTypeS", "AbilityStoneBattleRaritySellTypeA", "AbilityStoneBattleRaritySellTypeS", "InCombat", "WorkOutEndTime", "DoubleWorkOutEndTime", "HasRecommendNotice", "IsAutoSpecialSkill", "IsAutoOverDrive", "EnableConnect", "EnableIndividualAutoSell", "ImageQualitySetting", "RankingTitleId", "EquipType", "RaritySettingB", "RaritySettingA", "RaritySettingS", "AbilityStoneRaritySettingA", "AbilityStoneRaritySettingS", "AutoSellequipEvolution", "SoundeMute", "BattleAuto") VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (userid, username['DisplayUserId'], None, 0, 500, 500, 500, 500, False, 5, 5, 5, 3, 10201, None, None, None, None, False, True, None, None, None, False, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, None, None, 0, 0, 0, 0, 0, 0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, False, None, None, False, True, True, True, False, 1, None, None, None, None, None, None, None, False, 0))
        conn.commit()

        cur.execute(f"select * from userpref where userid = {(userid)}")
        sql = json.dumps(cur.fetchone(), default=str)
        sql = json.loads(sql)

        return {
            "r": sql,
            "t": ["up"],
            "st": systime(),
            "cm": None
        }
    else:
        return {
            "r": sql,
            "t": ["up"],
            "st": systime(),
            "cm": None
        }
    ...

def myPref(data, userid):
    # cur.execute(f"select * from public.userpref where userid = {int(userid)}")
    # sql = json.dumps(cur.fetchone())
    # sql = json.loads(sql)
    cur.execute(f'''update userpref SET {", ".join(f'"{k}"={v}' for k, v in data.items())} where userid = {int(userid)}''')
    conn.commit()
    
    cur.execute(f"select * from public.userpref where userid = {int(userid)}")
    sql = json.dumps(cur.fetchone())
    sql = json.loads(sql)

    return {
            "r": sql,
            "t": ["up"],
            "st": systime(),
            "cm": None
        }

def TutorialUpdate(status, userid):
    cur.execute(f'''update userpref SET "TutorialStatus"={int(status)} where userid = {int(userid)}''')
    conn.commit()

    return {
            "r": {},
            "t": ["up"],
            "st": systime(),
            "cm": None
        }
    ...

def bonusLogin(userid):
    print(userid)
    cur.execute(f'select "CurrentLoginCount", "LatestLogin", "HasSeenChanceRoulette" from public.users where "Id" = {int(userid)}')
    sql = json.dumps(cur.fetchone())
    sql = json.loads(sql)
    print(sql)
    
    if datetime.fromtimestamp(sql['LatestLogin']).date() == datetime.now().date():
        return {"LoginBonus" : [],
            "ConvertGachaMedalResult": {
                "ExpiredGachaMedalQuantity": 0,
                "ResultMistPeiceQuantity": 0
            },
            "HasSeenChanceRoulette": sql['HasSeenChanceRoulette'],
            "MayExpireItems": {
                "MayExpirePaidGems": [],
                "MayExpireLimitedItems": []
            },
            "LoginMovies": []}
    else:
        cur.execute(f'''update users SET "CurrentLoginCount"={int(sql['CurrentLoginCount'] + 1)}, "LatestLogin"={datetime.now().timestamp()}, "HasSeenChanceRoulette"={False}  where "Id" = {int(userid)}''')
        conn.commit()
        cur.execute(f'select "CurrentLoginCount", "LatestLogin" from public.users where "Id" = {int(userid)}')
        sql = json.dumps(cur.fetchone())
        sql = json.loads(sql)

        return {
            "LoginBonus": [
                {
                    "Id": 1,
                    "CurrentLoginCount": sql['CurrentLoginCount'],
                    "Order": 0,
                    "Title": "{\"EN\":\"Login Bonus\", \"TW\":\"登入報酬\", \"CN\":\"登入报酬\"}",
                    "IsLoop": 1,
                    "MCharacterId": None,
                    "NavigationText": "Here's your login bonus! You've received a shipment of goods addressed to the SSS. I've put them in the cargo van, so be sure to check it out♪",
                    "NavigationVoicePath": "Sounds\\Voices\\Characters\\Bases\\0\\voice_login_01.mp3",
                    "BackgroundImagePath": None,
                    "StartDate": "2021-01-01T15:00:00",
                    "EndDate": "2099-12-31T04:59:59",
                    "BonusType": 1,
                    "Items": [
                        {
                            "ItemId": 0,
                            "ItemType": 6,
                            "ItemQuantity": 10000,
                            "LoginCount": 1,
                            "UserItemId": 0,
                            "Sold": False
                        },
                        {
                            "ItemId": 73,
                            "ItemType": 4,
                            "ItemQuantity": 10,
                            "LoginCount": 2,
                            "UserItemId": 0,
                            "Sold": False
                        },
                        {
                            "ItemId": 0,
                            "ItemType": 7,
                            "ItemQuantity": 100,
                            "LoginCount": 3,
                            "UserItemId": 0,
                            "Sold": False
                        },
                        {
                            "ItemId": 11,
                            "ItemType": 4,
                            "ItemQuantity": 1,
                            "LoginCount": 4,
                            "UserItemId": 0,
                            "Sold": False
                        },
                        {
                            "ItemId": 14,
                            "ItemType": 4,
                            "ItemQuantity": 1,
                            "LoginCount": 5,
                            "UserItemId": 0,
                            "Sold": False
                        },
                        {
                            "ItemId": 5,
                            "ItemType": 4,
                            "ItemQuantity": 3,
                            "LoginCount": 6,
                            "UserItemId": 0,
                            "Sold": False
                        },
                        {
                            "ItemId": 78,
                            "ItemType": 4,
                            "ItemQuantity": 5,
                            "LoginCount": 7,
                            "UserItemId": 0,
                            "Sold": False
                        },
                        {
                            "ItemId": 0,
                            "ItemType": 6,
                            "ItemQuantity": 10000,
                            "LoginCount": 8,
                            "UserItemId": 0,
                            "Sold": False
                        },
                        {
                            "ItemId": 73,
                            "ItemType": 4,
                            "ItemQuantity": 10,
                            "LoginCount": 9,
                            "UserItemId": 0,
                            "Sold": False
                        },
                        {
                            "ItemId": 0,
                            "ItemType": 7,
                            "ItemQuantity": 100,
                            "LoginCount": 10,
                            "UserItemId": 0,
                            "Sold": False
                        },
                        {
                            "ItemId": 11,
                            "ItemType": 4,
                            "ItemQuantity": 1,
                            "LoginCount": 11,
                            "UserItemId": 0,
                            "Sold": False
                        },
                        {
                            "ItemId": 14,
                            "ItemType": 4,
                            "ItemQuantity": 1,
                            "LoginCount": 12,
                            "UserItemId": 0,
                            "Sold": False
                        },
                        {
                            "ItemId": 5,
                            "ItemType": 4,
                            "ItemQuantity": 3,
                            "LoginCount": 13,
                            "UserItemId": 0,
                            "Sold": False
                        },
                        {
                            "ItemId": 78,
                            "ItemType": 4,
                            "ItemQuantity": 5,
                            "LoginCount": 14,
                            "UserItemId": 0,
                            "Sold": False
                        },
                        {
                            "ItemId": 0,
                            "ItemType": 7,
                            "ItemQuantity": 100,
                            "LoginCount": 15,
                            "UserItemId": 0,
                            "Sold": False
                        }
                    ]
                },
                {
                    "Id": 43,
                    "CurrentLoginCount": sql['CurrentLoginCount'],
                    "Order": 999,
                    "Title": "{\"EN\":\"Sunny May Login Bonus\", \"TW\":\"梅雨晴日登入報酬\", \"CN\":\"梅雨晴日登入报酬\"}",
                    "IsLoop": 0,
                    "MCharacterId": 45401,
                    "NavigationText": "It's a lovely sunny day before the rainy season. It's best to wear pants that make you feel fresh♪",
                    "NavigationVoicePath": None,
                    "BackgroundImagePath": None,
                    "StartDate": "2022-05-15T05:00:00",
                    "EndDate": "2022-05-25T23:59:59",
                    "BonusType": 2,
                    "Items": [
                        {
                            "ItemId": 0,
                            "ItemType": 7,
                            "ItemQuantity": 300,
                            "LoginCount": 1,
                            "UserItemId": 0,
                            "Sold": False
                        },
                        {
                            "ItemId": 0,
                            "ItemType": 7,
                            "ItemQuantity": 300,
                            "LoginCount": 2,
                            "UserItemId": 0,
                            "Sold": False
                        },
                        {
                            "ItemId": 0,
                            "ItemType": 7,
                            "ItemQuantity": 300,
                            "LoginCount": 3,
                            "UserItemId": 0,
                            "Sold": False
                        },
                        {
                            "ItemId": 0,
                            "ItemType": 7,
                            "ItemQuantity": 300,
                            "LoginCount": 4,
                            "UserItemId": 0,
                            "Sold": False
                        },
                        {
                            "ItemId": 0,
                            "ItemType": 7,
                            "ItemQuantity": 300,
                            "LoginCount": 5,
                            "UserItemId": 0,
                            "Sold": False
                        },
                        {
                            "ItemId": 0,
                            "ItemType": 7,
                            "ItemQuantity": 300,
                            "LoginCount": 6,
                            "UserItemId": 0,
                            "Sold": False
                        },
                        {
                            "ItemId": 0,
                            "ItemType": 7,
                            "ItemQuantity": 300,
                            "LoginCount": 7,
                            "UserItemId": 0,
                            "Sold": False
                        }
                    ]
                },
                {
                    "Id": 44,
                    "CurrentLoginCount": sql['CurrentLoginCount'],
                    "Order": 999,
                    "Title": "{\"EN\":\"May Treasure Support Login Bonus\", \"TW\":\"5月寶藏應援登入報酬\", \"CN\":\"5月宝藏应援登入报酬\"}",
                    "IsLoop": 0,
                    "MCharacterId": 77301,
                    "NavigationText": "The desert is calming ...... I'm glad my first assignment was here. I am nervous but I will do my best.",
                    "NavigationVoicePath": None,
                    "BackgroundImagePath": None,
                    "StartDate": "2022-05-16T05:00:00",
                    "EndDate": "2022-05-25T23:59:59",
                    "BonusType": 2,
                    "Items": [
                        {
                            "ItemId": 261,
                            "ItemType": 4,
                            "ItemQuantity": 10,
                            "LoginCount": 1,
                            "UserItemId": 0,
                            "Sold": False
                        },
                        {
                            "ItemId": 261,
                            "ItemType": 4,
                            "ItemQuantity": 10,
                            "LoginCount": 2,
                            "UserItemId": 0,
                            "Sold": False
                        },
                        {
                            "ItemId": 261,
                            "ItemType": 4,
                            "ItemQuantity": 10,
                            "LoginCount": 3,
                            "UserItemId": 0,
                            "Sold": False
                        },
                        {
                            "ItemId": 261,
                            "ItemType": 4,
                            "ItemQuantity": 10,
                            "LoginCount": 4,
                            "UserItemId": 0,
                            "Sold": False
                        },
                        {
                            "ItemId": 261,
                            "ItemType": 4,
                            "ItemQuantity": 10,
                            "LoginCount": 5,
                            "UserItemId": 0,
                            "Sold": False
                        },
                        {
                            "ItemId": 261,
                            "ItemType": 4,
                            "ItemQuantity": 10,
                            "LoginCount": 6,
                            "UserItemId": 0,
                            "Sold": False
                        },
                        {
                            "ItemId": 261,
                            "ItemType": 4,
                            "ItemQuantity": 10,
                            "LoginCount": 7,
                            "UserItemId": 0,
                            "Sold": False
                        },
                        {
                            "ItemId": 261,
                            "ItemType": 4,
                            "ItemQuantity": 10,
                            "LoginCount": 8,
                            "UserItemId": 0,
                            "Sold": False
                        },
                        {
                            "ItemId": 261,
                            "ItemType": 4,
                            "ItemQuantity": 10,
                            "LoginCount": 9,
                            "UserItemId": 0,
                            "Sold": False
                        },
                        {
                            "ItemId": 261,
                            "ItemType": 4,
                            "ItemQuantity": 10,
                            "LoginCount": 10,
                            "UserItemId": 0,
                            "Sold": False
                        }
                    ]
                }
            ],
            "ConvertGachaMedalResult": {
                "ExpiredGachaMedalQuantity": 0,
                "ResultMistPeiceQuantity": 0
            },
            "HasSeenChanceRoulette": False,
            "MayExpireItems": {
                "MayExpirePaidGems": [],
                "MayExpireLimitedItems": []
            },
            "LoginMovies": []
        }

def updateChanceRoulette(userid):
    cur.execute(f'select "HasSeenChanceRoulette" from public.users where "Id" = {int(userid)}')
    sql = json.dumps(cur.fetchone())
    sql = json.loads(sql)
    cur.execute(f'''update users SET "HasSeenChanceRoulette"={True}, "LatestLogin"={datetime.now().timestamp()} where "Id" = {int(userid)}''')
    conn.commit()
    return 



   


def id_generator(size=12, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/Content/Js")
async def main():
    return FileResponse("./fd-mistglobal-prod-ntk.azurefd.net/Content/Js", media_type="application/javascript")

@app.get("/prod-client-web-ntk/src/project.js")
async def main():
    return FileResponse("./cdn2-mistglobal-prod-ntk.azureedge.net/prod-client-web-ntk/src/project.js", media_type="application/javascript")

@app.get("/prod-client-web-ntk/cocos2d-js-min.js")
async def main():
    return FileResponse("./cdn2-mistglobal-prod-ntk.azureedge.net/prod-client-web-ntk/cocos2d-js-min.js", media_type="application/javascript")

#### Login at loading, need hosted to VPS
@app.post("/api/DMM/auth")
async def loginorRegister(request: Request):
    # print(Header())
    # print(await request.body())
    jss = {
        "sub": "1",
        "cnt": "5",
        "__gameVersion": "2",
        "__userLoginGameDate": "5/21/2022 5:00:00 AM",
        "nbf": 1653159230,
        "exp": 1653245630,
        "iat": 1653159230,
        "iss": "kms3.com",
        "aud": "dmm"
    }
    token = jwt.encode(jss, "privateserver", algorithm="HS256")
    return {
        "r": token,
        "t":None,
        "st": systime(),
        "cm":None
    }

#### Implemented with Function
@app.get("/api/Users/{item}")
async def read_item(item, authorization: Union[str, None] = Header(default=None)):
    if item == "Me":
        #Check if exist:
        token = authorization.replace("Bearer ", "")
        userid = jwt.decode(token, options={"verify_signature": False}, algorithms=["HS256"])['sub']
        print(type(userid))
        print(userid)
        cur.execute(f'''SELECT "Id", "DateOfBirth", "CurrentActionPoints", to_char("ActionPointsRestoredAt"::timestamp, 'YYYY-MM-DD"T"HH24:MI:SS') AS "ActionPointsRestoredAt", "IsAdult", "Money", "Gem", "FreeGem", "Level", "TotalExperience", "MaxActionPoints", "TotalFieldSkillCost", "DisplayUserId", "CurrentLoginCount", "LatestLogin", "HasSeenChanceRoulette" from public.users where "Id" = {int(userid)}''')
        try:
            sql = json.dumps(cur.fetchone(), default=str)
            sql = json.loads(sql)
        except:
            sql = None
        if sql == None:

            cur.execute(f"""
INSERT INTO public.users("Id", "DateOfBirth", "CurrentActionPoints", "ActionPointsRestoredAt", "IsAdult", "Money", "Gem", "FreeGem", "Level", "TotalExperience", "MaxActionPoints", "TotalFieldSkillCost", "DisplayUserId", "CurrentLoginCount", "LatestLogin") VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (userid, None, 25, systime(), True, 10000, 1000, 1000, 1, 0, 25, 20, id_generator(), 0, datetime.strptime("1970-01-02 10:00:00", "%Y-%m-%d %H:%M:%S").timestamp()))
            conn.commit()
            cur.execute(f'''SELECT "Id", "DateOfBirth", "CurrentActionPoints", to_char("ActionPointsRestoredAt"::timestamp, 'YYYY-MM-DD"T"HH24:MI:SS') AS "ActionPointsRestoredAt", "IsAdult", "Money", "Gem", "FreeGem", "Level", "TotalExperience", "MaxActionPoints", "TotalFieldSkillCost", "DisplayUserId", "CurrentLoginCount", "LatestLogin", "HasSeenChanceRoulette" from public.users where "Id" = {int(userid)}''')
            a = json.dumps(cur.fetchone(), default=str)
            print(a)
            a = json.loads(a)

            me = {
                "r": sql,
                "t": None,
                "st": systime(),
                "cm": None
            }
        
            return me
        else:
            me = {
                "r": sql,
                "t": None,
                "st": systime(),
                "cm": None
            }
            return me
    elif item == "MyPreferences":
        token = authorization.replace("Bearer ", "")
        userid = jwt.decode(token, options={"verify_signature": False}, algorithms=["HS256"])['sub']

        return getPref(userid)

@app.post("/api/Users/MyPreferences")
def save_pref(data: dict, authorization: Union[str, None] = Header(default=None)):
    pprint(data)
    token = authorization.replace("Bearer ", "")
    userid = jwt.decode(token, options={"verify_signature": False}, algorithms=["HS256"])['sub']
    
    return myPref(data, userid)

@app.post("/api/Users/Tutorial/Update")
async def read_item(tutorialStatus: int, authorization: Union[str, None] = Header(default=None)):
    print(tutorialStatus)
    token = authorization.replace("Bearer ", "")
    userid = jwt.decode(token, options={"verify_signature": False}, algorithms=["HS256"])['sub']

    return TutorialUpdate(tutorialStatus, userid)

@app.post("/api/Login")
async def login(authorization: Union[str, None] = Header(default=None)):
    token = authorization.replace("Bearer ", "")
    userid = jwt.decode(token, options={"verify_signature": False}, algorithms=["HS256"])['sub']

    r = bonusLogin(userid)
    BonusLogin = {
        "r": r,
        "t": None,
        "st": systime(),
        "cm": None
    }
    return BonusLogin

###  Partial Working
@app.post("/api/ChanceRoulette/update")
async def main(authorization: Union[str, None] = Header(default=None)):
    token = authorization.replace("Bearer ", "")
    userid = jwt.decode(token, options={"verify_signature": False}, algorithms=["HS256"])['sub']
    updateChanceRoulette(userid)
    return {
        "r": {
            "PrizeRank": 7,
            "Rewards": [{
                "ItemType": 7,
                "ItemQuantity": 500,
                "ItemId": 0,
                "UserItemId": 0,
                "Sold": False
            }]
        },
        "t": None,
        "st": systime(),
        "cm": None
    }

##### Not implemented yet
@app.get("/api/{item}")
async def read_item(item):
    if item == "Quests":
        
        return {"r":[],"t":None,"st":systime(),"cm":None}
    elif item == "Home":
        return {
            "r": {
                "MissionCount": 0,
                "PresentCount": 1,
                "FriendMeterMaxCount": 0,
                "HasUnrecognizedFriendRequests": False,
                "HasFinalizablePayments": False,
                "HasNewestNews": True,
                "IsMarketLineupUpdate": True,
                "HasTenDaysLoginMissionBadge": True,
                "HasNewOrUnreadCharaScenario": False,
                "HasNewHomeNotice": False,
                "HideFreeTutorialFlags": 0,
                "Banners": [{
                    "BannerType": 0,
                    "JumpScene": 3,
                    "Path": "treasure009",
                    "StartDate": "2022-05-16T05:00:00",
                    "EndDate": "2022-05-21T04:59:59",
                    "DisplayStartDate": None,
                    "DisplayEndDate": "2022-05-25T23:59:59",
                    "Priority": None,
                    "TargetValue": 47,
                    "WebLinkUrl": None
                }, {
                    "BannerType": 0,
                    "JumpScene": 5,
                    "Path": "traning008",
                    "StartDate": "2022-05-11T05:00:00",
                    "EndDate": "2022-05-20T23:59:59",
                    "DisplayStartDate": None,
                    "DisplayEndDate": "2022-05-20T23:59:59",
                    "Priority": None,
                    "TargetValue": 46,
                    "WebLinkUrl": None
                }, {
                    "BannerType": 1,
                    "JumpScene": 13,
                    "Path": "20220518_linkskill_gacha_pichup_today",
                    "StartDate": "2022-05-18T05:00:00",
                    "EndDate": "2022-05-27T23:59:59",
                    "DisplayStartDate": None,
                    "DisplayEndDate": None,
                    "Priority": None,
                    "TargetValue": 400001,
                    "WebLinkUrl": None
                }, {
                    "BannerType": 1,
                    "JumpScene": 12,
                    "Path": "20210518_gachaticket_pack",
                    "StartDate": "2022-05-18T05:00:00",
                    "EndDate": "2022-05-24T23:59:59",
                    "DisplayStartDate": None,
                    "DisplayEndDate": None,
                    "Priority": None,
                    "TargetValue": 10047,
                    "WebLinkUrl": None
                }, {
                    "BannerType": 1,
                    "JumpScene": 13,
                    "Path": "20210517_544UHF7SIPSD_gacha_pichup_today",
                    "StartDate": "2022-05-16T05:00:00",
                    "EndDate": "2022-05-29T23:59:59",
                    "DisplayStartDate": None,
                    "DisplayEndDate": None,
                    "Priority": None,
                    "TargetValue": 1029,
                    "WebLinkUrl": None
                }, {
                    "BannerType": 1,
                    "JumpScene": 11,
                    "Path": "commom_support_jewelpack",
                    "StartDate": "2022-05-16T05:00:00",
                    "EndDate": "2022-05-20T23:59:59",
                    "DisplayStartDate": None,
                    "DisplayEndDate": None,
                    "Priority": None,
                    "TargetValue": None,
                    "WebLinkUrl": None
                }, {
                    "BannerType": 1,
                    "JumpScene": 12,
                    "Path": "20210516_ticket_pack",
                    "StartDate": "2022-05-16T05:00:00",
                    "EndDate": "2022-05-29T23:59:59",
                    "DisplayStartDate": None,
                    "DisplayEndDate": None,
                    "Priority": None,
                    "TargetValue": 10034,
                    "WebLinkUrl": None
                }, {
                    "BannerType": 1,
                    "JumpScene": 12,
                    "Path": "20210515_change_8yqjsu6BEgsx_satsukibare",
                    "StartDate": "2022-05-15T05:00:00",
                    "EndDate": "2022-05-25T04:59:59",
                    "DisplayStartDate": None,
                    "DisplayEndDate": None,
                    "Priority": None,
                    "TargetValue": 260,
                    "WebLinkUrl": None
                }, {
                    "BannerType": 1,
                    "JumpScene": 12,
                    "Path": "20210511_skill_khi8HUJmVTBy_messina",
                    "StartDate": "2022-05-11T05:00:00",
                    "EndDate": "2022-06-01T23:59:59",
                    "DisplayStartDate": None,
                    "DisplayEndDate": None,
                    "Priority": None,
                    "TargetValue": 252,
                    "WebLinkUrl": None
                }, {
                    "BannerType": 1,
                    "JumpScene": 12,
                    "Path": "common_choushuchu",
                    "StartDate": "2022-05-11T05:00:00",
                    "EndDate": "2022-05-20T23:59:59",
                    "DisplayStartDate": None,
                    "DisplayEndDate": None,
                    "Priority": None,
                    "TargetValue": None,
                    "WebLinkUrl": None
                }, {
                    "BannerType": 1,
                    "JumpScene": 12,
                    "Path": "20220511_skill_vh3jxrd9yrwf_Orleans",
                    "StartDate": "2022-05-11T05:00:00",
                    "EndDate": "2022-05-24T23:59:59",
                    "DisplayStartDate": None,
                    "DisplayEndDate": None,
                    "Priority": None,
                    "TargetValue": 20024,
                    "WebLinkUrl": None
                }, {
                    "BannerType": 1,
                    "JumpScene": 12,
                    "Path": "20210503_uxYb0oD3QYOF_order",
                    "StartDate": "2022-05-03T05:00:00",
                    "EndDate": "2022-05-31T23:59:59",
                    "DisplayStartDate": None,
                    "DisplayEndDate": None,
                    "Priority": None,
                    "TargetValue": None,
                    "WebLinkUrl": None
                }, {
                    "BannerType": 1,
                    "JumpScene": 12,
                    "Path": "20210501_Wvlw1kXkmFaK_newlayerpack",
                    "StartDate": "2022-05-01T05:00:00",
                    "EndDate": "2022-06-01T23:59:59",
                    "DisplayStartDate": None,
                    "DisplayEndDate": None,
                    "Priority": None,
                    "TargetValue": 248,
                    "WebLinkUrl": None
                }, {
                    "BannerType": 1,
                    "JumpScene": 12,
                    "Path": "common_xgyT9GfVyKHP_mikifuda",
                    "StartDate": "2022-05-01T05:00:00",
                    "EndDate": "2022-09-01T04:59:59",
                    "DisplayStartDate": None,
                    "DisplayEndDate": None,
                    "Priority": None,
                    "TargetValue": 222,
                    "WebLinkUrl": None
                }, {
                    "BannerType": 1,
                    "JumpScene": 11,
                    "Path": "onetimegempack",
                    "StartDate": "2021-01-01T15:00:02",
                    "EndDate": "2099-12-31T23:59:59",
                    "DisplayStartDate": None,
                    "DisplayEndDate": None,
                    "Priority": None,
                    "TargetValue": 4,
                    "WebLinkUrl": None
                }, {
                    "BannerType": 1,
                    "JumpScene": 101,
                    "Path": "discord_banner",
                    "StartDate": "2021-01-01T15:00:00",
                    "EndDate": "2099-01-01T04:59:59",
                    "DisplayStartDate": None,
                    "DisplayEndDate": None,
                    "Priority": None,
                    "TargetValue": None,
                    "WebLinkUrl": None
                }],
                "IsBeginnerMissionComplete": False,
                "BeginnerMissionInfo": {
                    "CompleteCount": 0,
                    "CurrentMMissionId": 609000001,
                    "IsCurrentMissionComplete": False
                },
                "SpeechViewModels": [{
                    "MCharacterBaseId": 10,
                    "MCharacterId": 10201,
                    "MHomeSpeechId": 3103
                }, {
                    "MCharacterBaseId": 10,
                    "MCharacterId": 10201,
                    "MHomeSpeechId": 3102
                }, {
                    "MCharacterBaseId": 10,
                    "MCharacterId": 10201,
                    "MHomeSpeechId": 3109
                }],
                "FooterEventIconViwModels": [],
                "CurrentOpenRecommendShops": None,
                "TenDaysMissonRetensionViewModel": {
                    "IsRetentionInLoginHome": False,
                    "TotalReciveLoginGem": 0,
                    "RecivedGemPurchasedPack": 0,
                    "TotalClearMissionCount": 0,
                    "RemainLoginMissionItemCount": 0,
                    "RecievedGemPurchasedPackSet": 0
                },
                "LotteryCampaignViewModel": None,
                "PanelMissions": None
            },
            "t": None,
            "st": systime(),
            "cm": None
        }

    elif item == "UItems":
        return {
            "r": [{
                "Id": 4321595,
                "MItemId": 261,
                "Stock": 10
            }],
            "t": None,
            "st": systime(),
            "cm": None
        }

    elif item == "UItemsByMItemIds":
        return {
            "r": [],
            "t": None,
            "st": "2022-05-19T04:47:36",
            "cm": None
        }
    
    elif item == "GetUMissionProgresses":
        return {
            "r": [{
                "Id": 47114479,
                "MMissionId": 101000001,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114480,
                "MMissionId": 101000002,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114481,
                "MMissionId": 101000003,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114482,
                "MMissionId": 101000004,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114483,
                "MMissionId": 101000005,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114484,
                "MMissionId": 101000006,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114485,
                "MMissionId": 101000007,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114486,
                "MMissionId": 106000063,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114487,
                "MMissionId": 106000064,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114488,
                "MMissionId": 106000065,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114489,
                "MMissionId": 106000066,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114490,
                "MMissionId": 202000001,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114491,
                "MMissionId": 202000011,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114492,
                "MMissionId": 202000016,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114493,
                "MMissionId": 202000021,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114494,
                "MMissionId": 202000026,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114495,
                "MMissionId": 202000031,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114496,
                "MMissionId": 202000034,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114497,
                "MMissionId": 202000037,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114498,
                "MMissionId": 202000047,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114499,
                "MMissionId": 202000048,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114500,
                "MMissionId": 303000026,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114501,
                "MMissionId": 303000041,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114502,
                "MMissionId": 303000059,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114503,
                "MMissionId": 303000064,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114504,
                "MMissionId": 303000069,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114505,
                "MMissionId": 303000074,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114506,
                "MMissionId": 303000080,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114507,
                "MMissionId": 303000082,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114508,
                "MMissionId": 303000087,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114509,
                "MMissionId": 303000092,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114510,
                "MMissionId": 303000097,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114511,
                "MMissionId": 303000102,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114512,
                "MMissionId": 303000107,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114513,
                "MMissionId": 303000112,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114514,
                "MMissionId": 303000124,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114515,
                "MMissionId": 303000145,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114516,
                "MMissionId": 303000156,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114517,
                "MMissionId": 303000168,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114518,
                "MMissionId": 303000226,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114519,
                "MMissionId": 303000238,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114520,
                "MMissionId": 303000250,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114521,
                "MMissionId": 303000262,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114522,
                "MMissionId": 303000274,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114523,
                "MMissionId": 303000289,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114524,
                "MMissionId": 303000304,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114525,
                "MMissionId": 303000319,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114526,
                "MMissionId": 303000334,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114527,
                "MMissionId": 303000349,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114528,
                "MMissionId": 303000364,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114529,
                "MMissionId": 303000386,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114530,
                "MMissionId": 303000408,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114531,
                "MMissionId": 303000430,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114532,
                "MMissionId": 303000452,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114533,
                "MMissionId": 303000468,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114534,
                "MMissionId": 303000484,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114535,
                "MMissionId": 303000500,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114536,
                "MMissionId": 303000516,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114537,
                "MMissionId": 303000532,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114538,
                "MMissionId": 303000548,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114539,
                "MMissionId": 303000564,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114540,
                "MMissionId": 303000580,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114541,
                "MMissionId": 303000596,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114542,
                "MMissionId": 303000612,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114543,
                "MMissionId": 303000628,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114544,
                "MMissionId": 303000644,
                "Count": 1,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114545,
                "MMissionId": 303000659,
                "Count": 1,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114546,
                "MMissionId": 303000674,
                "Count": 1,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114547,
                "MMissionId": 303000689,
                "Count": 1,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114548,
                "MMissionId": 303000704,
                "Count": 1,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114549,
                "MMissionId": 303000719,
                "Count": 1,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114550,
                "MMissionId": 303000734,
                "Count": 1,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114551,
                "MMissionId": 303000749,
                "Count": 1,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114552,
                "MMissionId": 303000764,
                "Count": 1,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114553,
                "MMissionId": 303000779,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114554,
                "MMissionId": 303000780,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114555,
                "MMissionId": 303000781,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114556,
                "MMissionId": 303000782,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114557,
                "MMissionId": 303000783,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114558,
                "MMissionId": 303000784,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114559,
                "MMissionId": 303000785,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114560,
                "MMissionId": 303000786,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114561,
                "MMissionId": 303000787,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114562,
                "MMissionId": 303000788,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114563,
                "MMissionId": 303000790,
                "Count": 1,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114564,
                "MMissionId": 303000902,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114565,
                "MMissionId": 303000903,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114566,
                "MMissionId": 506000364,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114567,
                "MMissionId": 506000365,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114568,
                "MMissionId": 506000366,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114569,
                "MMissionId": 506000386,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114570,
                "MMissionId": 506000392,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114571,
                "MMissionId": 507050290,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114572,
                "MMissionId": 507050291,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114573,
                "MMissionId": 507050292,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114574,
                "MMissionId": 507050302,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114575,
                "MMissionId": 507050312,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114576,
                "MMissionId": 609000001,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114577,
                "MMissionId": 609000002,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114578,
                "MMissionId": 609000003,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114579,
                "MMissionId": 609000004,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114580,
                "MMissionId": 609000005,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114581,
                "MMissionId": 609000006,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114582,
                "MMissionId": 609000007,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114583,
                "MMissionId": 609000008,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114584,
                "MMissionId": 609000009,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114585,
                "MMissionId": 609000010,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114586,
                "MMissionId": 609000011,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114587,
                "MMissionId": 609000012,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114588,
                "MMissionId": 609000013,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114589,
                "MMissionId": 609000014,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114590,
                "MMissionId": 609000015,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114591,
                "MMissionId": 609000016,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114592,
                "MMissionId": 609000017,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114593,
                "MMissionId": 609000018,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114594,
                "MMissionId": 609000019,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114595,
                "MMissionId": 609000020,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114596,
                "MMissionId": 609000021,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114597,
                "MMissionId": 609000022,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114598,
                "MMissionId": 609000023,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114599,
                "MMissionId": 609000024,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114600,
                "MMissionId": 609000025,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114601,
                "MMissionId": 609000026,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114602,
                "MMissionId": 609000029,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114603,
                "MMissionId": 609000030,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114604,
                "MMissionId": 609000031,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114605,
                "MMissionId": 609000032,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114606,
                "MMissionId": 609000033,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114607,
                "MMissionId": 609000034,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114608,
                "MMissionId": 609000035,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114609,
                "MMissionId": 609000036,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114610,
                "MMissionId": 609000037,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114611,
                "MMissionId": 609000038,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114612,
                "MMissionId": 609000039,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114613,
                "MMissionId": 609000041,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114614,
                "MMissionId": 609000042,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114615,
                "MMissionId": 609000043,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114616,
                "MMissionId": 609000044,
                "Count": 1,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114617,
                "MMissionId": 609000045,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114618,
                "MMissionId": 609000046,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114619,
                "MMissionId": 609000047,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114620,
                "MMissionId": 609000048,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114621,
                "MMissionId": 609000049,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114622,
                "MMissionId": 609000050,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114623,
                "MMissionId": 609000051,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114624,
                "MMissionId": 609000052,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114625,
                "MMissionId": 609000053,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114626,
                "MMissionId": 609000055,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114627,
                "MMissionId": 609000056,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114628,
                "MMissionId": 609000057,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114629,
                "MMissionId": 609000059,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114630,
                "MMissionId": 609000060,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114631,
                "MMissionId": 609000061,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114632,
                "MMissionId": 609000062,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114633,
                "MMissionId": 609000063,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114634,
                "MMissionId": 609000064,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114635,
                "MMissionId": 609000065,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114636,
                "MMissionId": 609000066,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114637,
                "MMissionId": 609000067,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114638,
                "MMissionId": 609000068,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114639,
                "MMissionId": 609000069,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114640,
                "MMissionId": 609000071,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114641,
                "MMissionId": 609000072,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114642,
                "MMissionId": 609000073,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114643,
                "MMissionId": 609000074,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }, {
                "Id": 47114644,
                "MMissionId": 609000075,
                "Count": 0,
                "CompletedAt": None,
                "RewardAcquired": False
            }],
            "t": None,
            "st": systime(),
            "cm": None
        }
    
    elif item == "GetTenDaysUMissionProgresses":
        return {
            "r": {
                "Id": 0,
                "MMissionId": 0,
                "Count": 0,
                "Stock": 0,
                "TendaysMItemPackId": 4,
                "TendaysSetMItemPackId": 33,
                "IsCompletedMission": False,
                "ExpiredAt": None
            },
            "t": None,
            "st": systime(),
            "cm": None
        }

@app.get("/api/Worlds/{item}")
async def read_item(item):
    if item == "AreasWithChapterUnlockQuest":
        return {
    "r": {
        "AreaDifficulties": [{
            "MAreaId": 1,
            "ClearDifficultiesCount": 0
        }],
        "MUnlockQuestControlId": None
    },
    "t": None,
    "st": systime(),
    "cm": None
}

@app.post("/api/UPayments/{item}")
async def read_item(item):
    if item == "purchaseResult":
        return FileResponse("./fd-mistglobal-prod-ntk.azurefd.net/api/UPayments/purchaseResult3", media_type="application/json")

@app.get("/api/UScenes/{scene}")
async def read_item(scene):
    return FileResponse(f".assets/scene/{scene}", media_type="application/json")


@app.get("/api/Users/Tutorial/GetHideFreeTutorialFlags")
async def main():
    return "ok"

@app.post("/api/UGachas/{subpath}/DoRollTutorialGacha")
async def main(subpath):
    if subpath == "Tutorial":
        now = datetime.now()

        tutorial_gacha = {
            "r": {
                "ReceivedItems": {
                    "Items": [
                        {
                            "UserItemId": 9691957,
                            "ItemId": 24301,
                            "ItemType": 8,
                            "ItemQuantity": 1,
                            "Sold": False
                        },
                        {
                            "UserItemId": 9691959,
                            "ItemId": 7201,
                            "ItemType": 8,
                            "ItemQuantity": 1,
                            "Sold": False
                        },
                        {
                            "UserItemId": 9691960,
                            "ItemId": 2201,
                            "ItemType": 8,
                            "ItemQuantity": 1,
                            "Sold": False
                        },
                        {
                            "UserItemId": 9691961,
                            "ItemId": 18201,
                            "ItemType": 8,
                            "ItemQuantity": 1,
                            "Sold": False
                        },
                        {
                            "UserItemId": 9691962,
                            "ItemId": 31201,
                            "ItemType": 8,
                            "ItemQuantity": 1,
                            "Sold": False
                        },
                        {
                            "UserItemId": 9691963,
                            "ItemId": 22201,
                            "ItemType": 8,
                            "ItemQuantity": 1,
                            "Sold": False
                        },
                        {
                            "UserItemId": 9691964,
                            "ItemId": 11201,
                            "ItemType": 8,
                            "ItemQuantity": 1,
                            "Sold": False
                        },
                        {
                            "UserItemId": 9691965,
                            "ItemId": 33201,
                            "ItemType": 8,
                            "ItemQuantity": 1,
                            "Sold": False
                        },
                        {
                            "UserItemId": 9691966,
                            "ItemId": 27201,
                            "ItemType": 8,
                            "ItemQuantity": 1,
                            "Sold": False
                        },
                        {
                            "UserItemId": 9691958,
                            "ItemId": 10301,
                            "ItemType": 8,
                            "ItemQuantity": 1,
                            "Sold": False
                        }
                    ],
                    "GiftItems": [],
                    "DeletedItemIds": []
                },
                "ReceivedBonusItems": {
                    "Items": [],
                    "GiftItems": [],
                    "DeletedItemIds": []
                }
            },
            "t": None,
            "st": now.strftime("%Y-%m-%dT%H:%M:%S"),
            "cm": None
        }
        
        return tutorial_gacha
    else:
        raise HTTPException(status_code=403, detail="Not Implemented yet!")

@app.get("/api/UGiftBoxes/{item}")
async def main(item):
    if item == "False":
        return {
            "r": [],
            "t": None,
            "st": systime(),
            "cm": None
        }
    elif item == "true":
        return {
            "r": [{
                "UInboxId": 2229181,
                "Title": "Welcome to Private server",
                "Description": "This server is supported by NexiaMoe",
                "GiftBoxItemViewModels": [{
                    "ItemId": 5,
                    "ItemType": 4,
                    "ItemQuantity": 10,
                    "UserItemId": 0,
                    "Sold": False
                }],
                "CreatedAt": "2022-05-19T12:22:04.8666667",
                "UpdatedAt": "2022-05-19T12:22:04.8666667"
            }],
            "t": None,
            "st": systime(),
            "cm": None
        }

@app.get("/api/Home/{item}")
async def main(item):
    if item == "GetHomeNotice":
        return {
            "r": [{
                "Id": 346,
                "ImagePath": "20210501_Wvlw1kXkmFaK_newlayerpack",
                "Order": 3420,
                "AlreadyRead": True
            }, {
                "Id": 347,
                "ImagePath": "20210503_uxYb0oD3QYOF_order",
                "Order": 3440,
                "AlreadyRead": True
            }, {
                "Id": 351,
                "ImagePath": "20210506_6d6xZywaCeS5_roulette",
                "Order": 3450,
                "AlreadyRead": True
            }, {
                "Id": 355,
                "ImagePath": "20210511_J3rtFLSCSycj_training_today",
                "Order": 3570,
                "AlreadyRead": True
            }, {
                "Id": 356,
                "ImagePath": "common_choushuchu",
                "Order": 3550,
                "AlreadyRead": True
            }, {
                "Id": 357,
                "ImagePath": "20210511_3F6AQf7Sh473_gacha_5stp_premium_today",
                "Order": 3540,
                "AlreadyRead": True
            }, {
                "Id": 358,
                "ImagePath": "20210511_skill_khi8HUJmVTBy_messina",
                "Order": 3560,
                "AlreadyRead": True
            }, {
                "Id": 360,
                "ImagePath": "20210515_change_8yqjsu6BEgsx_satsukibare",
                "Order": 3590,
                "AlreadyRead": True
            }, {
                "Id": 363,
                "ImagePath": "20210517_L5n5MgHBYATE_premium_update",
                "Order": 3630,
                "AlreadyRead": True
            }, {
                "Id": 364,
                "ImagePath": "20210517_qeCe5gnuGiCR_treasure_today",
                "Order": 3660,
                "AlreadyRead": True
            }, {
                "Id": 365,
                "ImagePath": "20210517_544UHF7SIPSD_gacha_pichup_abilityimg",
                "Order": 3640,
                "AlreadyRead": True
            }, {
                "Id": 366,
                "ImagePath": "20210517_544UHF7SIPSD_gacha_pichup_today",
                "Order": 3650,
                "AlreadyRead": True
            }, {
                "Id": 100066,
                "ImagePath": "20220511_skill_vh3jxrd9yrwf_Orleans",
                "Order": 3530,
                "AlreadyRead": True
            }, {
                "Id": 100068,
                "ImagePath": "20210511_support_jewelpack",
                "Order": 3620,
                "AlreadyRead": True
            }, {
                "Id": 100070,
                "ImagePath": "20220518_linkskill_gacha_pichup_today",
                "Order": 3680,
                "AlreadyRead": True
            }, {
                "Id": 100074,
                "ImagePath": "20210516_ticket_pack",
                "Order": 3635,
                "AlreadyRead": True
            }, {
                "Id": 100085,
                "ImagePath": "20210518_gachaticket_pack",
                "Order": 3685,
                "AlreadyRead": True
            }],
            "t": None,
            "st": systime(),
            "cm": None
        }

@app.post('/api/Home/UpdateHomeNotice')
async def updateHome():
    return {
        "r": True,
        "t": None,
        "st": systime(),
        "cm": None
    }

# @app.get("/Videos/Tutorial/{video}")
# async def sendvideo(video):
#     return 
# https://cdn2-mistglobal-prod-ntk.azureedge.net/prod-client-web-assets-ntk1-8-1/Videos/Tutorial/prologue.mp4?/xF3bdN2z1TSdNgM8VJCqA==
