import discord
import Helper
import DiscordRiotBot as Bot
def switch(msg):
    if msg[1:6]=='match':
        check = msg[7:].split(" ")
        
        
    elif msg[1:8]=='history':
        check = msg[9:].split(" ")
        Helper.getPuuidFromUser(check[0], check[1], check[2][1:])
        
        
        
async def send_message(message, user_message, is_private):
    try:
        response=switch(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)
        

    
def run_bot():
    TOKEN = ''
    
    intents= discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents = intents)
    
    @client.event
    async def on_ready():
        print(f'{client.user} started')
        
    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)
        
        if(user_message[0]== '+'):
            user_message=user_message[1:]
            
            await send_message(message, user_message, is_private = True)
        else:
            await send_message(message, user_message, is_private = False)
            
    client.run(TOKEN)