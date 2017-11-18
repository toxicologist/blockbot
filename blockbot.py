#!/usr/bin/python3
import discord, requests, json, random, asyncio, time, sys, os
from discord.ext.commands import Bot
from discord.ext import commands

blockbot = Bot(command_prefix="!")
bheighturl = ("http://chancoin.info/api/getblockcount")
bheight = requests.get(bheighturl)
hashrateurl = ("http://chancoin.info/api/getnetworkhashps")
diffurl = ("http://chancoin.info/api/getdifficulty")
supplyurl= ("https://www.blockexperts.com/api?coin=4chn&action=getmoneysupply")
i = 0
tracking = False

def percentage(whole, part):
  return 100 * float(part)/float(whole)

def getRoll():
    roll = random.randint(10000000,99999999)
    return roll

def has_doubles(n,dub):
    return(len(set((str(n))[-dub:])) < 2)

def get():
    f = getRoll()

    #dubs,trips,quads,quints
    if (has_doubles(f,5)):
        print("%s is your roll - you get QUINTS!!!"%(str(f)))
    elif (has_doubles(f,4)):
        print("%s is your roll - you get QUADS!!!"%(str(f)))
    elif (has_doubles(f,3)):
        print("%s is your roll - you get TRIPS!!"%(str(f)))
    elif (has_doubles(f,2)):
        print("%s is your roll - you get DUBS!"%(str(f)))
    else:
        print("%s is your roll"%(str(f)))

def bytes_2_human_readable(number_of_bytes):
    if number_of_bytes < 0:
        raise ValueError("!!! numberOfBytes can't be smaller than 0 !!!")

    step_to_greater_unit = 1000.

    number_of_bytes = float(number_of_bytes)
    unit = 'bytes'

    if (number_of_bytes / step_to_greater_unit) >= 1:
        number_of_bytes /= step_to_greater_unit
        unit = 'kh/s'

    if (number_of_bytes / step_to_greater_unit) >= 1:
        number_of_bytes /= step_to_greater_unit
        unit = 'mh/s'

    if (number_of_bytes / step_to_greater_unit) >= 1:
        number_of_bytes /= step_to_greater_unit
        unit = 'gh/s'

    if (number_of_bytes / step_to_greater_unit) >= 1:
        number_of_bytes /= step_to_greater_unit
        unit = 'th/s'

    precision = 3
    number_of_bytes = round(number_of_bytes, precision)

    return str(number_of_bytes) + ' ' + unit

@blockbot.event
async def on_ready():
    print("Client logged in")
    await blockbot.change_presence(game=discord.Game(name='with chancoin'))
    
#@blockbot.command("help")
#async def help():
    #return await blockbot.say("Hello! I am ChanBot. My commands are:\n!currentblock - Returns the current block number\n!hashrate - Returns the network hashrate as of the last block.\n!difficulty - Returns the current block's difficulty.\n!supply - Returns the current total supply of Chancoins.\n!blockinfo - Returns useful information about the current block.")

"""@blockbot.command("enable-tracking")
async def enabletracking():
    global tracking
    if tracking != True:
        await blockbot.say("Tracking has been enabled. I will now check if we have hit a new block every 10 seconds.")
        tracking = True
        block_old = (requests.get(bheighturl)).text
        block_new = (requests.get(bheighturl)).text
        #block_old = 0
        #block_new = 1
        while True:
            block_new = (requests.get(bheighturl)).text
            if block_old != block_new:
                await blockbot.say("@toxicologist#8641 We've reached a new block! New block is %s, old block was %s."%(block_new,block_old))
            blockbot_old = (requests.get(bheighturl)).text
            await asyncio.sleep(10)
    else:
        await blockbot.say("Tracking is already enabled.")
        
@blockbot.command("disable-tracking")
async def disabletracking():
    global tracking
    if tracking != False:
        await blockbot.say("Tracking has been disabled.")
        tracking = False
    else:
        await blockbot.say("Tracking is already disabled.")
"""
@blockbot.command("currentblock")
async def getcurrentblock():
    bheight = requests.get(bheighturl)
    return await blockbot.say("Current block is %s."%bheight.text)

#@blockbot.command("hashrate")
#async def getcurrenthashrate():
#    hashrate = requests.get(hashrateurl)
#    hashrate_ghs = bytes_2_human_readable(int(hashrate.text))
#    return await blockbot.say("Hashrate as of the last block is %s."%hashrate_ghs)

@blockbot.command("difficulty")
async def getcurrentdiff():
    diff = requests.get(diffurl)
    return await blockbot.say("Difficulty is %s."%diff.text)

@blockbot.command("supply")
async def getcurrentsupply():
    supply = requests.get(supplyurl)
    return await blockbot.say("Total ChanCoin supply is %s coins, %s of which are community-mined (%s%% of the total supply)."%(int(float(supply.text)-3000000), int(float(supply.text)-9000000), str(percentage(float(supply.text)-3000000,int((float(supply.text)-9000000))))[:3]))

@blockbot.command("blockinfo")
async def getcurrentblockinfo():
    bheight = requests.get(bheighturl)
    hashrated = requests.get(hashrateurl)
    hashrate = bytes_2_human_readable(int(hashrated.text))
    diff = requests.get(diffurl)
    return await blockbot.say("We are at block %s, with a difficulty of %s and %s of network power."%(bheight.text, diff.text, hashrate))

@blockbot.command("time")
async def timeremaining():
    hashrate = requests.get(hashrateurl)
    diff = requests.get(diffurl)
    time = (float(diff.text)*2**32)/(float(hashrate.text))
    hashrate_ghs = bytes_2_human_readable(int(hashrate.text))
    m, s = divmod(time, 60)
    h, m = divmod(m, 60)
    await blockbot.say("Current block should take %d hours, %d minutes and %d seconds to complete, assuming that difficulty is %s and hashrate is %s."%(h,m,s,diff.text,hashrate_ghs))

@blockbot.command("explorer")
async def sendexplorerlink():
    return await blockbot.say("http://chancoin.info")

@blockbot.command("general")
async def sendcurrentgeneral():
    return await blockbot.say("http://boards.4chan.org/biz/chancoin")

@blockbot.command("download")
async def senddownloadlink():
    return await blockbot.say("http://bit.ly/2udYUYE")

@blockbot.command("badmeme")
async def badmeme():
    return await blockbot.say("That was a bad meme and you should feel bad.\n" + "-1.0000 4CHN has been deducted from the memer's wallet.")

#@blockbot.command("tip")
#async def tipme():
#    return await blockbot.say("If you enjoy this bot, send tips to CXbaYoKVDWfyXPC4aJaw1KgTPoGxWasov2! Thanks <3")

#@blockbot.command("edgar")
#async def edgar():
#	i = random.randint(0,25)
#	file = ('%d.png'%i)
#	with open(file, 'rb') as f:
#		await blockbot.send_file(discord.Object(id='339071711737675787'), f)
#		
@blockbot.command("goodbot")
async def goodbot():
	return await blockbot.say("<3")

@blockbot.command("badbot")
async def badbot():
        return await blockbot.say(":(")

@blockbot.command("areyougay")
async def gay():
        return await blockbot.say("No, only gay person here is Megu")

"""@blockbot.command("autobot")
async def test():
    await blockbot.say("I will now automatically send updates about the blockchain every 20 minutes.")
    while True:
        bheight = requests.get(bheighturl)
        hashrate = requests.get(hashrateurl)
        diff = requests.get(diffurl)
        await blockbot.say("We are at block %s, with a difficulty of %s and %s gH/s of network power."%(bheight.text, diff.text, hashrate.text))
        await asyncio.sleep(1200)"""

@blockbot.command("triforce")
async def triforce():
    await blockbot.say("Newfags can't do this")
    await asyncio.sleep(0.2)
    await blockbot.say("‌  ‌ ▲\n▲‌ ▲")

@blockbot.command("goodbye")
async def bye():
    await blockbot.say("Goodbye guys. Restarting..")
    os.execv(__file__, sys.argv)

@blockbot.command("exchanges")
async def exchanges():
    await blockbot.say("http://bit.ly/2t08oD9 - Tradesatoshi")
    await blockbot.say("http://bit.ly/2vm81U3 - Novaexchange")
	
@blockbot.command("marketcap")
async def marketcap():
    f = requests.get('https://api.coinmarketcap.com/v1/ticker/chancoin/')
    f = json.loads(f.text)[0]
    ff = float(f['market_cap_usd'])
    fint = int(ff)
    await blockbot.say("Current marketcap in USD is $%d."%fint)

@blockbot.command("volume")
async def volume():
    f = requests.get('https://api.coinmarketcap.com/v1/ticker/chancoin/')
    f = json.loads(f.text)[0]
    f = f['24h_volume_usd']
    await blockbot.say("Trading volume of the last 24 hours is $%s."%f)

@blockbot.command("price")
async def price():
    f = requests.get('https://api.coinmarketcap.com/v1/ticker/chancoin/')
    f= json.loads(f.text)[0]
    p_btc = f['price_btc']
    p_usd = f['price_usd']
    return await blockbot.say("Current ChanCoin price is $%s and %s BTC (%s%% change in the last 24h)."%(p_usd, p_btc, f['percent_change_24h']))

coinminers = requests.get("http://coinminers.net/api/stats/")
uj=coinminers.json()
ujchan = uj["pools"]["chancoin"]

#blockbot = Bot(command_prefix="!")

#@blockbot.event
#async def on_ready():
#    print("Client logged in")

@blockbot.command("hashrate")
async def hashratecheck():
#    hashrate = requests.get(hashrateurl)
#    hashrate_ghs = bytes_2_human_readable(int(hashrate.text))
#    return await blockbot.say("Hashrate as of the last block is %s."%hashrate_ghs)
    hashrate=requests.get(hashrateurl)
    hashrate_ghs = bytes_2_human_readable(int(hashrate.text))
    await blockbot.say("Hashrate as of the last block is %s."%hashrate_ghs)
    string = ("**Coinminers.net workers: **%s\n"%ujchan["workerCount"])
    for worker in ujchan["workers"]:
        string += ("\n**%s**: %s"%(worker,ujchan["workers"][worker]["hashrateString"]))
    string += ("\n\n**Total hashpower (Coinminers):** %s"%ujchan["hashrateString"])
    return await blockbot.say(string)

blockbot.run("MzM1MDkzODkzMDA1ODM2Mjg4.DJ7Myw.m9T7DIQj2SaaKkhaDmuru35qKmU")

