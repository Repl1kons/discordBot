import asyncio

import discord
from discord.ext import commands
import config
from discord import utils
client = discord.Client()

# bot = commands.Bot(command_prefix='!')

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message_for_user(self, message):
        print('Message from {0.author}: {0.content}'.format(message))


@client.event
async def on_message(message):
    id = client.get_guild(config.ID)
    badwords = ["еблан","лох", "пидор", "нацист", "уебан", "пидорас", "пидарас", "ебал", "ебальник", "хуй", "пизда",
                "шлюха", "подьебал", "выебал", "уебал", "сьебал", "съебал", "пизди", "пиздишь", "пиздабол", "пиздаплет"]
    unwarnusers = ["Dyno#3861", "Carl-bot#1536", "MEE6#4876", "Charlzerx#9889"]
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

                if warns == 5:
                    user = await client.fetch_user(user_id=664225659278852148)
                    await user.send(f'пользователь {message.author.mention}, непристойно себя ведет на сервере Rebzi, вот его сообщение:  \n{message.content}\nНарушение было в канале {message.channel}. \n Нарушение: {warns}')


                await channel.send(f"__________________________________________________\nЗа человеком {message.author.mention} было замечено нарушение.\nВот его сообщение: \n{message.content}\nНарушение было в канале {message.channel}. \n Нарушение: {warns}")
client.run(config.token)




# @bot.command()
# async def ping(message):
#     await message.send('pong')
#
# bot.run(token)
