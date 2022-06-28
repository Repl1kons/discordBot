import discord
from discord.ext import commands
from discord import utils
import config


class get_role(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @commands.command(name="text", help="sas")
    @commands.has_role('Admin')
    async def text(self, ctx):
        for ch in self.bot.get_guild(ctx.guild.id).channels:
            if ch.name == "получение-ролей":
                emb = discord.Embed(title=f"чтобы получить роль и открыть\nдля себя доступ только к нужными каналам,\nвыберите соответствующую реакцию из списка:\n\n1.  😥 - тильт\n2. 🎮 - геймер\n3. 🎨 - UX/UI дизайнер\n4. 🖥 - программист\n5. 🎧 - чилллл", colour=discord.Colour.green())
                emb.set_footer(text=f'Выбрать можно только 3 роли')
                await ctx.channel.purge(limit=1)
                message = await ctx.send(embed = emb)
                for emoji in ['😥', '🎮', '🎨', '🖥️', '🎧']:
                    await message.add_reaction(emoji)





    @commands.Cog.listener()
    async def on_raw_reaction_add(self, ctx):
        channel = self.bot.get_channel(ctx.channel_id)
        message = await channel.fetch_message(ctx.message_id)
        member = utils.get(message.guild.members, id=ctx.user_id)

        try:
            emoji = str(ctx.emoji)
            role = utils.get(message.guild.roles, id=config.ROLES[emoji])

            if(len([i for i in member.roles if i.id not in config.EXCROLES]) <= config.MAX_ROLES_PER_USER):
                await member.add_roles(role)

            else:
                await message.remove_reaction(ctx.emoji, member)

        except KeyError as e:
            a = e

        except Exception as e:
            a = e

    ################################################################ АВТО-ЗАБИРАНИЕ РОЛИ  ###############################################################
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, ctx):
        channel = self.bot.get_channel(ctx.channel_id)  # получаем объект канала
        message = await channel.fetch_message(ctx.message_id)  # получаем объект сообщения
        member = utils.get(message.guild.members, id=ctx.user_id)  # получаем объект пользователя который поставил реакцию

        try:
            emoji = str(ctx.emoji)  # эмоджик который выбрал юзер
            role = utils.get(message.guild.roles, id=config.ROLES[emoji])  # объект выбранной роли (если есть)

            await member.remove_roles(role)


        except KeyError as e:
            a = e
        except Exception as e:
            a = e

def setup(client):
    client.add_cog(get_role(client))