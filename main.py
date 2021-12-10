import discord
from discord.ext import commands
import config

intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    game = discord.Game("Minecraft!")
    await client.change_presence(status=discord.Status.idle, activity=game)


@client.event
async def on_member_join(member):
    channel = client.get_channel(918118713050419210)
    await channel.send(f"hello {member} you came to the Rebzi server, thank you for being with us")

@client.event
async def on_member_remove(member):
    channel = client.get_channel(918118713050419210)
    await channel.send(f"Наш карабль под названием Rebzi потерпели утрату, нас покинул {member}")




@client.event
async def on_message(message):


    unwarnusers = ["Dyno#3861", "Carl-bot#1536", "MEE6#4876", "Charlzerx#9889"]
    channel_debug = client.get_channel(918976290479022201)

    if str(message.author) not in unwarnusers:
        await channel_debug.send(f"Logged in as {client.user} (ID: {client.user.id})\n"
                            f"Message from {message.author}: {message.content}\n"
                            f"_______________________\n")

    # with open("C:/Users/dubov/PycharmProjects/DiscordAdminBot/mainSpace/debugging.txt", "a") as debugging:
    #     debugging.write(f"Logged in as {client.user} (ID: {client.user.id})\n"
    #                     f"Message from {message.author}: {message.content}\n"
    #                     f"_______________________\n")
    #     debugging.close()





    if message.content == "!clear_debug" or message.content[:message.content.find(' ')] == '!clear_debug':
        # with open("C:/Users/dubov/PycharmProjects/DiscordAdminBot/mainSpace/debugging.txt", "w") as debugging:
        #     debugging.write(" ")
        #     debugging.close()
        await message.channel.purge(limit=100)
        await message.reply("Журнал отладки очищен")

    if message.content == "!all_commands" or message.content[:message.content.find(' ')] == '!all_commands':
        await message.channel.send(f"Команда !clear_debug очищает канал debuging (он доступен только для админов)\n"
                                   f"Команда !clear_all очищает список нарушителей сервера\n"
                                   f"Команда !clear @упоминание удаляет конкретного человека указаного после символа @ из списка нарушителей\n"
                                   f"Команда !clear_allmessage удаляет 100 сообщений в канале\n"
                                   f"Команда !warns выводит список нарушителей\n"
                                   f"Команда !all_commands выводит список всех команд этого бота")

    # id = client.get_guild(config.ID)
    badwords = ["еблан", "лох", "пидор", "нацист", "уебан", "пидорас", "пидарас", "ебал", "ебальник", "хуй", "пизда",
                "шлюха", "подьебал", "выебал", "уебал", "сьебал", "съебал", "пизди", "пиздишь", "пиздабол", "пиздаплет",
                "залупень", "залупа", "залупка"]

    if message.content == "!clearall" or message.content[:message.content.find(' ')] == '!clearall':
        warn_file = open("C:/Users/dubov/PycharmProjects/DiscordAdminBot/mainSpace/warns.txt", "w")
        warn_file.write("")
        warn_file.close()
        await message.channel.send('Все нарушители очищенны')

    if message.content == "!clear" or message.content[:message.content.find(' ')] == '!clear':
        if message.content == '!clear':
            await message.channel.send('Напишите !clear @упоминание')
        else:
            with open("C:/Users/dubov/PycharmProjects/DiscordAdminBot/mainSpace/warns.txt", "r") as wf:
                lines = wf.readlines()
            with open("C:/Users/dubov/PycharmProjects/DiscordAdminBot/mainSpace/warns.txt", "w") as wf:
                for line in lines:
                    if line.strip() != message.content[
                                       message.content.find(' '):].strip() and line.strip() != message.content[message.content.find(' '):].strip().replace('!', ""):
                        wf.write(line.strip(" "))
                await message.channel.send('Очищено!')

    if message.content == "!clear_allmessage" or message.content[:message.content.find(' ')] == '!clear_allmessage':
        await message.channel.purge(limit=100)

    if message.content == "!warns" or message.content[:message.content.find(' ')] == '!warns':
        warn_file = open("C:/Users/dubov/PycharmProjects/DiscordAdminBot/mainSpace/warns.txt", "r")
        warn_you = []
        for line in warn_file:
            warn_you.append(line.strip())
        warn_file.close()
        warns = 0
        for user in warn_you:
            if str(message.author.mention) == user:
                warns += 1
            await message.channel.send(f"______________________\nНарушители:\n" + '\n'.join(
                map(str, warn_you)) + f"\n______________________\nВаши нарушения: {warns}\n______________________")

    for word in badwords:
        if word in message.content.lower():
            if str(message.author) not in unwarnusers:
                warn_file = open("C:/Users/dubov/PycharmProjects/DiscordAdminBot/mainSpace/warns.txt", "a")
                warn_file.write(str(message.author.mention) + "\n")
                warn_file.close()
                warn_file = open("C:/Users/dubov/PycharmProjects/DiscordAdminBot/mainSpace/warns.txt", "r")
                warned_users = []
                for line in warn_file:
                    warned_users.append(line.strip())
                warn_file.close()
                warns = 0
                channel = await client.fetch_channel(917369108159397949)
                for user in warned_users:
                    if str(message.author.mention) == user:
                        warns += 1

                if warns == 4:
                    await channel.send(
                        f"__________________________________________________\nДорогой {message.author.mention} за вами было замечено непристойное поведение на данном сервере, не отправляйте сообщение с содержанием ненормативной лексики, иначе я отправлю ваше дело на рассмотрение модераторам!!!,\nНадеюсь вы меня поняли")

                if 5 <= warns <= 7:
                    user = await client.fetch_user(user_id=664225659278852148)
                    await user.send(
                        f'Пользователь {message.author.mention}, непристойно себя ведет на сервере Rebzi, вот его сообщение:  \n{message.content}\nНарушение было в канале {message.channel}. \n Нарушение: {warns}')

                await channel.send(
                    f"__________________________________________________\nЗа человеком {message.author.mention} было замечено нарушение.\nВот его сообщение: \n{message.content}\nНарушение было в канале {message.channel}. \n Нарушение: {warns}")

client.run(config.token)
