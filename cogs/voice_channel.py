# import discord
# from discord.ext import commands, tasks
#
#
# class Voice_join(commands.Cog):
#     def __init__(self, bot):
#         self.bot = bot
#
#     # @commands.command(name="add")
#     # async def create_voice(self, ctx):
#     @commands.Cog.listener()
#     async def on_voice_state_update(self, member, before, after):
#         guild = member.guild
#         author = member.message.author
#
#         # for category in guild.categories:
#         #     if category.name == 'chill':
#         #         voice_chats_category = category
#
#         if after.channel:
#             if after.channel.name == 'add':
#
#                 overwrites = {
#                     guild.default_role: discord.PermissionOverwrite(connect=False, view_channel=False),
#                     self.bot.user: discord.PermissionOverwrite(connect=True, view_channel=True,
#                                                                 manage_channels=True),
#                     member: discord.PermissionOverwrite(connect=True, view_channel=True, speak=True,
#                                                         mute_members=True)
#                 }
#                         # private_voice_chat = await guild.create_voice_channel(f'{member.display_name}\'s Private Duo chat!',
#                         #                                                       user_limit=2, overwrites=overwrites,
#                         #                                                       category=voice_chats_category)
#
#                 private_voice_chat = await guild.create_voice_channel(f"{member.author} channel", user_limit=4, overwrites=overwrites,
#                                                         category=discord.utils.get(guild.categories, name="chill"), reason=None)
#                 print(len(str(member)))
#                 await member.move_to(private_voice_chat)
#                 #
#                 # def check(a, b, c):
#                 #     return len(private_voice_chat.members) == 0
#                 #
#                 # await self.bot.wait_for('voice_state_update', check=check)
#                 # await private_voice_chat.delete()
#
#         if before.channel:
#             if before.channel.category.name == 'chill':
#                 if len(before.channel.members) == 0:
#                     if before.channel.name == 'New Talk':
#                         pass
#                     else:
#                         await before.channel.delete()
#         # await guild.create_voice_channel(f"{ctx.author} channel", overwrites=None, category=guild.categories[3], reason=None)
#         # category = await guild.create_category("Management", overwrites=None, reason=None)
#         # await guild.create_voice_channel(f"Member Count: {guild.member_count}", overwrites=None, category=category,
#         #                                  reason=None)
#
#
# def setup(client):
#     client.add_cog(Voice_join(client))
import discord
from discord.ext import commands
from discord import PermissionOverwrite, Member


class VoiceCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):

        # for guild in self.bot.guilds:
        #     for channel in guild.channels.category:
        #         print(channel)

        if after.channel:
            if after.channel.name == '➕ | game':
                public_category = after.channel.category
                public_channel = await after.channel.guild.create_voice_channel(name=f"{member.name}'s game room",
                                                                                category=public_category)
                await member.move_to(public_channel)

        if before.channel:
            if before.channel.category.name == '🔊голосовая🔊':
                if before.channel.name == f"{member.name}'s game room":
                    await before.channel.delete()

        if after.channel:
            if after.channel.name == '➕ | work':
                public_category = after.channel.category
                public_channel = await after.channel.guild.create_voice_channel(name=f"{member.name}'s work room",
                                                                                category=public_category)
                await member.move_to(public_channel)

        if before.channel:
            if before.channel.category.name == '🔊голосовая🔊':
                if before.channel.name == f"{member.name}'s work room":
                    await before.channel.delete()



        if after.channel:
            if after.channel.name == '➕ | chill':
                public_category = after.channel.category
                public_channel = await after.channel.guild.create_voice_channel(name=f"{member.name}'s chill room",
                                                                                category=public_category)
                await member.move_to(public_channel)

        if before.channel:
            if before.channel.category.name == '🔊голосовая🔊':
                if before.channel.name == f"{member.name}'s chill room":
                    await before.channel.delete()


    @commands.command(name="join_voice", help="Вы можете быстро подключиться к голосовому каналу друга без поиска его")
    async def joinsx(self, ctx, user: discord.Member):
        user = user or ctx.author
        member_voi = ctx.author.voice.channel

        await user.move_to(member_voi)


def setup(client):
    client.add_cog(VoiceCog(client))
