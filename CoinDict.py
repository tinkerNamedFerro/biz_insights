from kucoin_api.Kucoin import *
from coingecko.util import coinGeckoList

import json

commonTickerList = ["ONE"]

# Some ticker/coin name are just that fucking bad
blackList = ["JST" , "THT", "MUST", "COIN", "CAP","MEDIA", "TALK", "CHAIN", "ERC20", "STACK", "KEY", "FEAR", "USELESS", "NEAR", "SMART", "CUT", "START","KEEP", "NEAR","ROAD", "DATA", "STRING", "IDEA","ETF", "OPEN", "GAS", "ACT", "PLAY", "WAVES", "LOL", "SHA", "FORTH", "KSM", 
"UNI", "WILD", "HERO", "ELON", "OPEN", "ROUTE", "FLOW", "MASK", "SUPER","SCLP", "GO", "MATTER","MASK", "NFT", "TIME", "JST", 
"MAN", "FEAR", "LAYER", "WIN", "MOON","GOD", "YOU", "CARDS", "HELMET", "PART", "HARD",
 "BIT", "HE", "LIKE", "DUST", "SENSE", "COPS", "SPAM", "ALPHA", "STEP", "MINE", "FAIR", "TON", "CAPS", "CAP", "COPE", "CAKE", "BED", "MC", "ID", "PAPER", "GAINS", "SOUL", "RLY", "DIS", "" "HAPPY", "MEME", "SCRT", "ZERO", "SEEN", "ONES", "DEV", "RARE", "OWN", "TRUE", "SPELL", "PROB", "VISION", "FAST", "VID", "OIL", "TRUE", "MM", "ATM", "YOU", "GET","ADD", "SWAP","TRADE", "MOVE", "PAY", "FUN", "IF", "KEK", "WORLD", "LIKE", "START" "BOND", 
 "MARK", "BEACH", "JET", "ITS" "CRBN","🌐","LN","$BASED", "CUDOS", "XDC", "MINDS", "DIVER", "DEGEN", "TIPS", "WINGS", "ASAP", "MKR", "CCX", "ACE", "CQT", "APY","PLOT","GTH", "REL", "XCM", "FLUX", "MAID", "DUN", "CRE", "LINA", "RELAY", "RAZOR", "CCX" "SC", "HIT", "CITY", "SOCKS", "FOR", "REP", "PAR", "OXEN", "BLOCK", "BRD", "VOICE", "GHOST","STX", "ICE","REQ","HNS","MAP","RAMP", "GRID", "SUN", "CVC", "PCT", "SAKE", "BETA", "VAL", "NODE", "FLY", "PUSSY", "ZONE", "AUTO",  "PORT", "BEACH" "FOR","FREE", "SLAM", "PILOT", "BOOM", "HOT", "MERGE", "SPIRIT", "WING" ,"MILK", "BOND", "TRIBE", "JOE", "NEST", "MET", "MIX", "FIN", "DMD" ,"VERSE", "LA", "PINK", "OG", "DTA","D", "ZOOM", "MOONED", "COMBO", "DAWN", "FEED", "CORE", "FUEL", "CURE", "LEAD", "TORN", "BEAN", "PROS", "WOW", "MINT", "SOLAR", "ANGEL", "QUICK", "IQ", "METH", "INDEX", "FOLD", "FREE", "SYNC", "JEWEL", "COOK", "TEN", "COVER", "RABBIT", "HNST", "SAK3", "SAK", "KICK", "SALE", "RISE","DEX", "PAID", "MASS", "TREAT", "TECH", "BANANA", "STRK", "SANTA", "POP", "DOG", "MINT", "BID", "FREE", "YIELD", "WHITE", "RAT", "LAND", "UOS", "FINE", "BORING", "STRONG", "VALUE", "YLD", "NAME", "PRO", "VALUE", "MATH", "CAT", "VAULT", "SIX", "POT", "PEAK", "STAKE", "FARM", "AUCTION", "BOO" "FREE", "SXP", "FLOAT", "DIP", "HUNT", "WHALE", "TOP", "BAN", "LET", "PUT", "LAUNCH", "BET", "SURE", "EYE", "FEAR", "SOLD", "POOL", "LESS", "ANY", "CAP", "HODL", "EPIC", "BANK", "BUY", "PUSH", "FORM", "FRONT", "SNT", "CARD", "STND", "ASK"]

def generateCurrenciesList():
    # calling kucoin api to get all coins
    # currenciesResponse = getCurrencies()
    geckoCoinList = coinGeckoList()
    coins = []
    # Looping through coins to get ticker and name
    for row in geckoCoinList:
        ticker = row["symbol"].upper()
        name = row["name"].upper()
        commonTicker = False
        # If ticker is in blackList mark as so
        if ticker in commonTickerList:
            commonTicker = True
        if ticker not in blackList:
            coin = {"aka":[ticker], 'name':name, "commonTicker" : commonTicker, "coinGeckoId":row["id"]}
            coins.append(coin)


    # save all coins in json
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(coins, f, ensure_ascii=False, indent=4)
    

generateCurrenciesList()