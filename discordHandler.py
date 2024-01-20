import discord
import Helper
import json
import numpy as np
from api import TOKEN
from discord.ext import commands

matchBufferList=[]

def switch(msg) -> str:
    global matchBufferList
    #msg format: +match (game number)
    if msg[0:5]=='match':
        check = str(msg[6:].split(" "))
        check = check.replace("'", "")
        check = check.replace("[", "")
        check = check.replace("]", "")
        print(check)
        try:
            print('match')
            ret=Helper.getMatchInfo(matchBufferList[int(check)-1])
        except Exception as e:
            print(e)
            return "Error "+ str(e)
        return ret
        
    #msg format: +history na1 Chocomelk #Choco
    elif msg[0:7]=='history':
        check = msg[8:].split(" ")
        try:
            puuid = Helper.getPuuidFromUser(check[0], check[1], check[2][1:])
            print(puuid)
        except Exception as e:
            print(e)
            return "Error "+ str(e)
        try:
            matchBufferList=Helper.getMatches(puuid)
            print("worked "+ matchBufferList[0])
        except Exception as e:
            print(e)
            return "Error "+str(e)
        try:
            ret = Helper.printMatchList(matchBufferList, puuid)
            print(ret)
        except Exception as e:
            print(e)
            return "Error "+str(e)
        return ret

    #msg format: +profile na1 Chocomelk #Choco
    elif msg[0:7]=='profile':
        print("made it")
        check=msg[8:].split(" ")
        try:
            ret = Helper.getProfileData(check[0], check[1], check[2][1:])
            print(ret)
        except Exception as e:
            print(e)
            return "Error "+str(e)
        print("end")
        return ret
        
async def send_message(message, user_message, is_private):
    
    try:
        response=switch(user_message)
        #await message.author.send(response) if is_private else 
        await message.channel.send(response)
    except Exception as e:
        print(e)
    
def run_bot(): 
    intents= discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix="+", intents=discord.Intents.all())
    @bot.event
    async def on_ready():
        print(f'{bot.user} started')
        
    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return
        
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)
        
        if(user_message[0]== '+'):
            user_message=user_message[1:]
            await send_message(message, user_message, is_private = True)
        else:
            await send_message(message, user_message, is_private = False)
            
    bot.run(TOKEN)