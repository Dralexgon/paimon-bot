import discord
from discord.ext import commands

bot=commands.Bot(command_prefix="",description="Bot fun (créer par FireDragonAlex#0775)")

@bot.event
async def on_ready():
    print("Je suis prêt !")

@bot.event
async def on_message(message):
    ponctuation="?!."
    messageContent=message.content.lower()
    messageContent=messageContent.split(" ")
    if (messageContent[0]=="bonjour" or messageContent[0]=="salut") and messageContent[1]=="bot":
        await message.channel.send(f"Bonjour {message.author.name} !")
    for i in ponctuation:
        if messageContent[-1]==i:
            messageContent=messageContent[:len(messageContent)-1]
    if messageContent[-1]=="quoi":
        await message.channel.send(f"feur !")

token = open('../token.txt', 'r').readlines()[0]
bot.run(token)