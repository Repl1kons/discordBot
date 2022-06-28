import json
import sqlite3
import string
import discord
from discord.ext import commands


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        global base, cur
        base = sqlite3.connect('Bot.db')
        cur = base.cursor()
        if base:
            print("database connect, Все ок")

    @commands.command(name="Status", help="Status warnings", aliases=["status"])
    async def status(self, ctx):
        base.execute('CREATE TABLE IF NOT EXISTS {}(userid INT, count INT)'.format(ctx.message.guild.name))
        base.commit()
        warning = cur.execute('SELECT * FROM {} WHERE userid == ?'.format(ctx.message.guild.name),
                              (ctx.message.author.id,)).fetchone()
        if warning == None:
            await ctx.send(f"{ctx.message.author.mention}, У вас нет предупреждений!")
        #
        # if warning[1] == None:
        #     await ctx.send(f"{ctx.message.author.mention}, У вас нет предупреждений!")

        else:
            await ctx.send(f"{ctx.message.author.mention}, У вас {warning[1]} предупреждений!")

    # очистка таблицы
    @commands.command(name="Clwarn", help="Clear warnings (Only admin)", aliases=["clwarn"])
    @commands.has_role('Admin')
    async def clwarn(self, ctx):
        name = ctx.guild.name
        cur.execute('UPDATE {} SET count == ? WHERE userid == ?'.format(name), (1, ctx.author.id))
        base.commit()

        emb = discord.Embed(title="Очищенно", colour=discord.Colour.green())
        emb.add_field(name="Бот:",
                      value=f"Предупреждения за мат, были очищенны")
        emb.set_footer(text='Предупреждения были очищены по просьбе администратора {}'.format(ctx.author.name),
                       icon_url=ctx.author.avatar_url)

        await ctx.channel.send(embed=emb)

    @commands.Cog.listener()
    async def on_message(self, message, reason="Мат"):
        if not message.author.bot:
            if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in
                message.content.split(' ')}.intersection(set(json.load(open('cogs\jsonFiles\mat.json')))) != set():
                await message.delete()
                # создание таблицы
                name = message.guild.name

                base.execute('CREATE TABLE IF NOT EXISTS {}(userid INT, count INT)'.format(name))
                base.commit()

                warning = cur.execute('SELECT * FROM {} WHERE userid == ?'.format(name), (message.author.id,)).fetchone()

                if warning == None:
                    cur.execute('INSERT INTO {} VALUES(?, ?)'.format(name), (message.author.id, 1))
                    base.commit()
                    emb = discord.Embed(title="Нецензурная речь", icon_url=message.author.avatar_url,
                                        colour=discord.Colour.green())
                    emb.add_field(name="Бот:",
                                  value=f"{message.author.mention}, ваше предыдущее сообщение было удаленно по причине: Мат")
                    emb.set_author(name=message.author.name, icon_url=message.author.avatar_url)
                    emb.add_field(name="Предупреждение:",
                                  value=f"{message.author.mention}, первое предупреждение, на 3е - МУТ!")

                    await message.channel.send(embed=emb)

                elif warning[1] == 1:
                    cur.execute('UPDATE {} SET count == ? WHERE userid == ?'.format(name), (2, message.author.id))
                    base.commit()
                    emb = discord.Embed(title="Нецензурная речь", icon_url=message.author.avatar_url,
                                        colour=discord.Colour.green())
                    emb.add_field(name="Бот:",
                                  value=f"{message.author.mention}, ваше предыдущее сообщение было удаленноб по причине: Мат")
                    emb.set_author(name=message.author.name, icon_url=message.author.avatar_url)
                    emb.add_field(name="Предупреждение:",
                                  value=f"{message.author.mention}, второе предупреждение, еще раз вы отправите сообщение с матом и мы вас замьютим!")

                    await message.channel.send(embed=emb)

                elif warning[1] == 2:
                    cur.execute('UPDATE {} SET count == ? WHERE userid == ?'.format(name), (3, message.author.id))
                    base.commit()

                    emb = discord.Embed(title="Нецензурная речь", icon_url=message.author.avatar_url,
                                        colour=discord.Colour.green())
                    emb.add_field(name="Бот:",
                                  value=f"{message.author.mention}, был замьютен по причине: Мат")
                    emb.set_author(name=message.author.name, icon_url=message.author.avatar_url)
                    emb.add_field(name="Информирование:",
                                  value=f"Если пользователь пишет сообщение с матом, то на 3-е предупреждение его мьютят")

                    await message.channel.send(embed=emb)

                    guild = message.guild
                    mutedrole = discord.utils.get(guild.roles, name="Muted")

                    if not mutedrole:
                        mutedrole = await guild.create_role(name="Muted")

                        for ch in guild.channels:
                            await ch.set_permissions(mutedrole, speak=False, send_messages=False, read_message_history=True,
                                                     read_messages=True)
                    # time_warns = 5
                    await message.author.add_roles(mutedrole, reason=reason)

                    emb1 = discord.Embed(title="Нецензурная речь", icon_url=message.author.avatar_url,
                                         colour=discord.Colour.green())
                    emb1.add_field(name="Бот:",
                                   value=f"{message.author.mention}, Вы были замьчены по причине {reason}")
                    emb1.set_author(name=message.author.name, icon_url=message.author.avatar_url)
                    emb1.add_field(name="Информирование:",
                                   value=f"Если пользователь пишет сообщение с матом, то на 3-е предупреждение его мьютят")

                    await message.author.send(embed=emb1)
                # пытаюсь сделать мут на время
                # await asyncio.sleep(10)
                # await message.author.remove_roles(mutedrole)

    @commands.command(name="Report", aliases=["report"])
    async def report(self, ctx, user: discord.Member, *reason):
        guilds = ctx.guild
        for guildname in guilds.channels:
            if guildname.name == "адмнинистрация":
                channel = self.bot.get_channel(guildname.id)  # since it's a cog u need self.bot
                author = ctx.message.author
                rearray = ' '.join(reason[:])  # converts reason argument array to string
                if not rearray:  # what to do if there is no reason specified
                    await channel.send(f"Пользователь {author} недоволен поведением {user}, причина: есть")
                    await ctx.message.delete()  # I would get rid of the command input
                else:
                    await channel.send(f"Пользователь {author} недоволен поведением {user}, причина: {rearray}")
                    await ctx.message.delete()



def setup(bot):
    bot.add_cog(Moderation(bot))
