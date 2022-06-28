from io import BytesIO
import discord
from discord.ext import commands
from PIL import Image

class wanted_user(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("cogs: wanted -Ready!")

    @commands.command(name="Wanted", help="If you lost people, You will be found it", aliases=["wanted"])
    async def wanted(self, ctx, member: discord.Member = None):
        if not member:
            member = ctx.author

        wanted = Image.open("cogs/images/wanted.jpg")
        pfp = member.avatar_url_as(size=256)
        data = BytesIO(await pfp.read())
        pfp = Image.open(data)

        pfp = pfp.resize((960, 960))
        #                 влево, вверх
        wanted.paste(pfp, (227, 457))

        wanted.save("wanted-user.jpg")

        await ctx.reply(file=discord.File("cogs/images/wanted-user.jpg"))


def setup(bot):
    bot.add_cog(wanted_user(bot))
