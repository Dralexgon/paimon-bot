import collections
import discord
import asyncio
import sys
import time
from discord import user
from discord.ext import commands
from discord.message import Message
from discord.channel import TextChannel
from character import *
from random import randint

from csvLoadAndSave import loadCsv, saveCsv


def convertirDesSecondesEnJoursHeuresMinutesSecondes(secondeDeBase):
    jour,heure,minute,seconde=0,0,0,0
    jour=secondeDeBase//86400
    heure=(secondeDeBase-jour*86400)//3600
    minute+=(secondeDeBase-heure*3600)//60
    seconde=secondeDeBase-minute*60
    return (jour,heure,minute,seconde)

def getCharacterByName(name:str) -> Character:
    for character in allCharacters:
        if character.getName() == name:
            return character
    return None

def save():
    listOutput = []
    for character in allCharacters:
        for itemstack in character.inventory:
            tempList = []
            tempList.append(character.getName())
            tempList.append(itemstack.getAmount())
            tempList.append(itemstack.getType())
            listOutput.append(tempList)
    return listOutput

global prefix
prefix = "!p"
intents = discord.Intents.all()
#intents = discord.Intents.default()
intents.members = True

global allCommandes
allCommandes = {
    "help":"print all commands",
    "test":"answer test",
    "create":"create a character",
    "infos":"gives infos about your character",
    "infos {name}":"gives infos about {name}'s character",
    "collect {place}":"your character collect in {place}",
    "pay {name} {number} {thing}":"pay someone",
    "give {name} {number} {thing}":"give something to someone (only admin)"
}

global answersPaimon
answersPaimon = {
    "je m'ennuie":"Moi aussi, et si on mangeait ??",
    "merci":"De rien !"
}

global collectPaimon
collectPaimon = []

global allCharacters
allCharacters = []
bot=commands.Bot(command_prefix="!p ",description="Bot Paimon pour lapinou party (créer par FireDragonAlex)",intents=intents)

@bot.event
async def on_ready():
    global startBotTimeSamp
    startBotTimeSamp=time.time()
    print(f"[{round(time.time())}] [LOAD] Loading...")
    loadSuccefully,load=loadCsv("saves\\savesPaimon")
    if not(loadSuccefully):
        print(f"[{round(time.time())}] [ERROR] Load failed !")
        sys.exit()
    for l in load:
        name = l[0]
        character = getCharacterByName(name)
        if character == None:
            allCharacters.append(Character(name))
        else:
            character.setItemStackInventory(ItemStack(l[2],int(l[1])))
    print(f"[{round(time.time())}] [READY] I'm ready !")

@bot.command()
async def hello(ctx,*infos):
    message = await ctx.author.send("hello")
    await asyncio.sleep(1)
    await message.edit(content=f"hello {ctx.message.author.name} !")

@bot.command()
async def temps(ctx,*infos):
    print("test")
    temps=convertirDesSecondesEnJoursHeuresMinutesSecondes(time.time()-startBotTimeSamp)
    await ctx.channel.send(f"Temps depuis le démarrage du bot : {int(temps[0])}j, {int(temps[1])}h, {int(temps[2])}min et {int(temps[3])}s.")
    print("test2")

@bot.event
async def on_message(message:Message):
    ponctuation="?!."
    messageContent = message.content.lower()
    messageContent = messageContent.split(" ")
    
    if len(messageContent) > 1:
        if messageContent[0] == prefix:
            messageContent = messageContent[1:]
            print(f"[{round(time.time())}] [COMMANDS_EXECUTER] [{messageContent[0]}] by {message.author.name}")
            if messageContent[0] == "test":
                await message.channel.send("test")
                await message.channel.send("test: "+bot.command_prefix)
            if messageContent[0] == "temps":
                temps=convertirDesSecondesEnJoursHeuresMinutesSecondes(time.time()-startBotTimeSamp)
                await message.channel.send(f"Temps depuis le démarrage du bot : {int(temps[0])}j, {int(temps[1])}h, {int(temps[2])}min et {int(temps[3])}s.")
            if messageContent[0] == "pay":
                if len(messageContent) == 3 or len(messageContent) == 4:
                    messageContent = messageContent[1:]
                    #selectedMember = None
                    #print(member.discriminator)
                    for member in message.guild.members:
                        if messageContent[0] == member.name:
                            if len(messageContent) == 3 and int(messageContent[1]) > 0:
                                if getCharacterByName(message.author.name) == None:
                                    await message.channel.send(message.author.mention+" Tu dois créer un personnage !\n(!p create)")
                                    return
                                if getCharacterByName(member.name) == None:
                                    await message.channel.send(message.author.mention+f" {member.name} n'a pas de personnage !\n(!p create)")
                                    return
                                if getCharacterByName(message.author.name).getItemByType(messageContent[2]) == None:
                                    await message.channel.send(message.author.mention+f" Tu n'as pas de {messageContent[2]} !")
                                    return
                                try:
                                    int(messageContent[1])
                                except:
                                    await message.channel.send(message.author.mention+f" \"{messageContent[1]}\" n'est pas un nombre (entier) !")
                                    return
                                itemstack = getCharacterByName(message.author.name).getItemByType(messageContent[2])
                                if itemstack.getAmount() >= int(messageContent[1]):
                                    itemstack.setAmount(itemstack.getAmount()-int(messageContent[1]))
                                    getCharacterByName(member.name).addInventory(ItemStack(messageContent[2],int(messageContent[1])))
                                    await message.channel.send(message.author.mention+" La transaction a bien été effectuée !")
                                    print(f"[{round(time.time())}] [SAVE] Saving...")
                                    saveCsv("saves\\savesPaimon",save())
                                    return
                                else:
                                    await message.channel.send(message.author.mention+" Vous n'avez pas "+messageContent[1]+" mora !")
                                    return
                else:
                    await message.channel.send("Désolé, je n'ai pas compris.\n(!p pay {nom} {nombre} {chose})")
            if messageContent[0] == "create":
                messageContent = messageContent[1:]
                if len(messageContent) == 0:
                    if getCharacterByName(message.author.name) == None:
                        allCharacters.append(Character(message.author.name))
                        await message.channel.send(message.author.mention+" Votre personnage a bien été créé !")
                        print(f"[{round(time.time())}] [SAVE] Saving...")
                        saveCsv("saves\\savesPaimon",save())
                    else:
                        await message.channel.send(message.author.mention+" Votre personnage a déjà été créé !")
                if len(messageContent) == 1:
                    if messageContent[0] == "all":
                        nbCharacterCreate = 0
                        for member in message.guild.members:
                            if getCharacterByName(member.display_name) == None:
                                allCharacters.append(Character(member.display_name))
                                nbCharacterCreate += 1
                    await message.channel.send(f"{nbCharacterCreate} personnages ont bien été créés !")
                    print(f"[{round(time.time())}] [SAVE] Saving...")
                    saveCsv("saves\\savesPaimon",save())
            if messageContent[0] == "infos" or messageContent[0] == "info":
                if len(messageContent) == 1:
                    if getCharacterByName(message.author.name) == None:
                        await message.channel.send(message.author.mention+" Tu dois créer un personnage !\n(!p create)")
                    else:
                        character = getCharacterByName(message.author.name)
                        prepareSend = f"\n```Nom : {character.name}\nInventaire :"
                        for i in character.inventory:
                            prepareSend += f"\n--> {i.getAmount()} {i.getType()}"
                        prepareSend += "```"
                        await message.channel.send(message.author.mention+prepareSend)
                    return
                elif len(messageContent) == 2:
                    if messageContent[1] == "all":
                        for member in message.guild.members:
                            character = getCharacterByName(member.display_name)
                            prepareSend = f"\n```Nom : {character.name}\nInventaire :"
                            for i in character.inventory:
                                prepareSend += f"\n--> {i.getAmount()} {i.getType()}"
                            prepareSend += "```"
                            await message.channel.send(member.mention+prepareSend)
                    else:
                        if getCharacterByName(messageContent[1]) == None:
                            await message.channel.send(message.author.mention+f" {messageContent[1]} dois créer un personnage !\n(!p create)")
                        else:
                            character = getCharacterByName(messageContent[1])
                            prepareSend = f"\n```Nom : {character.name}\nInventaire :"
                            for i in character.inventory:
                                prepareSend += f"\n--> {i.getAmount()} {i.getType()}"
                            prepareSend += "```"
                            await message.channel.send(message.author.mention+prepareSend)
                else:
                    await message.channel.send("Désolé, je n'ai pas compris.\n(!p infos ou !p infos {nom})")
                return
            if messageContent[0] == "give":
                #for perm in message.author.guild_permissions:
                if str(message.author) == "FireDragonAlex#0775" or message.author.guild_permissions.administrator:
                    if len(messageContent) == 4:
                        try:
                            getCharacterByName(messageContent[1]).addInventory(ItemStack(messageContent[3],int(messageContent[2])))
                            await message.channel.send(f"{messageContent[1]} a bien reçu {int(messageContent[2])} {messageContent[3]} !")
                            print(f"[{round(time.time())}] [SAVE] Saving...")
                            saveCsv("saves\\savesPaimon",save())
                        except:
                            await message.channel.send("Désolé, je n'ai pas compris.\n(!p give {nom} {nombre} {chose})")
                    else:
                        await message.channel.send("Désolé, je n'ai pas compris.\n(!p give {nom} {nombre} {chose})")
                else:
                    await message.channel.send(f"Tu n'as pas la permission de give !")
                #if message.author.permissions_in
                #print(ItemStack(messageContent[3],int(messageContent[2])))
                #print(messageContent[1],messageContent[3],int(messageContent[2]))
                
                """
                elif len(messageContent) == 3:
                    getCharacterByName(message.author.name).addInventory(ItemStack(messageContent[2],int(messageContent[1])))
                    await message.channel.send(f"Vous avez bien reçu {int(messageContent[1])} {messageContent[2]})")
                """
            if messageContent[0] == "help":
                prepareSend = "```All paimon's commands :"
                for i in allCommandes.keys():
                    prepareSend += "\n- "+i+" : "+allCommandes[i]
                prepareSend += "```"
                await message.channel.send(prepareSend)
            if messageContent[0] == "collect":
                pass
            if messageContent[0] == "stop":
                if str(message.author) == "FireDragonAlex#0775" or message.author.guild_permissions.administrator:
                    print(f"[{round(time.time())}] [SAVE] Saving...")
                    saveCsv("saves\\savesPaimon",save())
                    await message.channel.send(message.author.mention+" Save !")
                    await message.channel.send(message.author.mention+" Disconnected !")
                    sys.exit()
                else:
                    await message.channel.send(f"Tu n'as pas la permission de stoper le bot !")
            if messageContent[0] == "save":
                print(f"[{round(time.time())}] [SAVE] Saving...")
                saveCsv("saves\\savesPaimon",save())
                await message.channel.send(message.author.mention+" Save !")
            if messageContent[0] == "rl":
                await message.channel.send(message.author.mention+" Error !")
                return
            if messageContent[0] == "clear":
                if message.author.guild_permissions.administrator:
                    oldMessages = await message.channel.history().flatten()
                    for oldMessage in oldMessages:
                        await oldMessage.delete()


    messageContent=message.content.lower()
    if messageContent == "cc" and message.author.display_name != bot.user.display_name:
        await message.channel.send("cc")
    if messageContent == "hehe":
        await message.channel.send("HEHE ? TE NANDAYO !!")
        await message.channel.send(file=discord.File('gifs\\tenandayo.gif'))
        #await message.channel.send(file=discord.File('gifs\\tenandayo.mp4'))
        await message.channel.send("(Je n'oublirai pas cet affront !)")
        #await message.channel.send("https://media.tenor.co/videos/5a8cc9477398eeb2a9d77152a97370ad/mp4")
    if messageContent == "casse croute d'urgence":
        await message.channel.send(file=discord.File('gifs\\cassecroute.mp4'))
    for k in answersPaimon.keys():
        if messageContent == k:
            await message.channel.send(answersPaimon[k])
    messageContent=messageContent.split(" ")
    if (messageContent[0]=="bonjour" or messageContent[0]=="salut") and (messageContent[1]=="bot" or messageContent[1]=="paimon"):
        await message.channel.send(f"Bonjour {message.author.name} !")
        return
    for i in messageContent:
        if i == "paimon":
            await message.channel.send("On parle de moi ??")
            await message.channel.send("On doit surement dire que je suis la plus belle et la plus intelligente !")
            await message.channel.send("PS : voici ma musique préférée ! https://r.mtdv.me/UjJ2bBHjhP")
    for i in ponctuation:
        if messageContent[-1]==i:
            messageContent=messageContent[:len(messageContent)-1]
    if messageContent[-1]=="quoi":
        await message.channel.send(f"feur !")

@bot.event
async def close():
    print(f"[{round(time.time())}] [SAVE] Saving...")
    saveCsv("saves\\savesPaimon",save())

token = open('../token.txt', 'r').readlines()[0]
bot.run(token)