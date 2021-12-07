# -*- coding: utf-8 -*-
import asyncio

import discord
from discord.ext import commands
import config
from discord import utils

import youtube_dl
import os
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from os import system
client = discord.Client()

# bot = commands.Bot(command_prefix='!')

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message_for_user(self, message):
        print('Message from {0.author}: {0.content}'.format(message))





@client.event
async def on_message(message):

    with open("C:/Users/dubov/PycharmProjects/DiscordAdminBot/mainSpace/debugging.txt", "a") as debuging:
            debuging.write(f"Logged in as {client.user} (ID: {client.user.id})\n"
                           f"Message from {message.author}: {message.content}\n"
                           f"----------------------------------------------------\n")

            debuging.close()




    if message.content == "$clear_debug" or message.content[:message.content.find(' ')] == '$clear_debug':
        with open("C:/Users/dubov/PycharmProjects/DiscordAdminBot/mainSpace/debugging.txt", "w") as debuging:
            debuging.write(" ")
            debuging.close()
            await message.reply("Журнал откладки очищен")

    unwarnusers = ["Dyno#3861", "Carl-bot#1536", "MEE6#4876", "Charlzerx#9889"]
    id = client.get_guild(config.ID)
    badwords = ["еблан","лох", "пидор", "нацист", "уебан", "пидорас", "пидарас", "ебал", "ебальник", "хуй", "пизда",
                "шлюха", "подьебал", "выебал", "уебал", "сьебал", "съебал", "пизди", "пиздишь", "пиздабол", "пиздаплет",
                "залупень", "залупа", "залупка"]


    if message.content == "$clearall" or message.content[:message.content.find(' ')] == '$clearall':
        warnFile = open("C:/Users/dubov/PycharmProjects/DiscordAdminBot/mainSpace/warns.txt", "w")
        warnFile.write("")
        warnFile.close()
        await message.channel.send('Все нарушители очищенны')



    if message.content == "$clear" or message.content[:message.content.find(' ')] == '$clear':
        if message.content == '$clear':
            await message.channel.send('Напишмте $clear @упоминание')
        else:
            with open("C:/Users/dubov/PycharmProjects/DiscordAdminBot/mainSpace/warns.txt", "r") as wf:
                lines = wf.readlines()
            with open("C:/Users/dubov/PycharmProjects/DiscordAdminBot/mainSpace/warns.txt", "w") as wf:
                for line in lines:
                    if line.strip() != message.content[message.content.find(' '):].strip() and line.strip() != message.content[message.content.find(' '):].strip().replace('!', ""):
                        wf.write(line.strip(" "))
                await message.channel.send('Очищено!')

    if message.content == "$clear_allmessage" or message.content[:message.content.find(' ')] == '$clear_allmessage':
        await message.channel.purge(limit=100)

    if message.content == "$warns" or message.content[:message.content.find(' ')] == '$warns':
        warnFile = open("C:/Users/dubov/PycharmProjects/DiscordAdminBot/mainSpace/warns.txt", "r")
        warnYou = []
        for line in warnFile:
            warnYou.append(line.strip())
        warnFile.close()
        warns = 0
        for user in warnYou:
            if str(message.author.mention) == user:
                warns+=1
            await message.channel.send(f"______________________\nНарушители:\n" + '\n'.join(map(str, warnYou)) + f"\n______________________\nВаши нарушения: {warns}\n______________________")



    for word in badwords:
        if word in message.content.lower():
            if str(message.author) not in unwarnusers:
                warnFile = open("C:/Users/dubov/PycharmProjects/DiscordAdminBot/mainSpace/warns.txt", "a")
                warnFile.write(str(message.author.mention) + "\n")
                warnFile.close()
                warnFile = open("C:/Users/dubov/PycharmProjects/DiscordAdminBot/mainSpace/warns.txt", "r")
                warnedUsers = []
                for line in warnFile:
                    warnedUsers.append(line.strip())
                warnFile.close()
                warns = 0
                channel = await client.fetch_channel(917369108159397949)
                for user in warnedUsers:
                    if str(message.author.mention) == user:
                        warns += 1

                if warns == 4:
                    await channel.send(f"__________________________________________________\nДорогой {message.author.mention} за вами было замечено непрестойное поведение на данном сервере, не отправляйте сообщение с содержанием ненормативной лексики, иначе я отправлю ваше дело на расмотрение модераторам!!!,\nНадеюсь вы меня поняли" )

                if warns >= 5 and warns <= 7:
                    user = await client.fetch_user(user_id=664225659278852148)
                    await user.send(f'пользователь {message.author.mention}, непристойно себя ведет на сервере Rebzi, вот его сообщение:  \n{message.content}\nНарушение было в канале {message.channel}. \n Нарушение: {warns}')


                await channel.send(f"__________________________________________________\nЗа человеком {message.author.mention} было замечено нарушение.\nВот его сообщение: \n{message.content}\nНарушение было в канале {message.channel}. \n Нарушение: {warns}")
client.run(config.token)




# @bot.command()
# async def ping(message):
#     await message.send('pong')
#
# bot.run(token)
