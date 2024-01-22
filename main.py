import os
import discord
from discord.ext import commands
from extenshions.program import settings
from cogs import levels, wanted

bot = commands.Bot(command_prefix='/', intents=discord.Intents.all())
bot.remove_command("help")


@bot.command(name='ping')
async def ping(ctx):
    ping = bot.latency
    emb = discord.Embed(description="Ща сек...", colour=discord.Color.orange())
    msg = await ctx.send(embed=emb)
    emb = discord.Embed(description=f'Pong! `{ping * 1000:.0f}ms` :ping_pong:', colour=discord.Color.orange())
    await msg.edit(embed=emb)
    print(f'[Logs] На данный момент пинг == {ping * 1000:.0f}ms | ping')

class MyHelp(commands.HelpCommand):
    """My very own help formatter"""

    async def send_bot_help(self, mapping):
        """Send this on [p]help without arguments"""
        channel = self.get_destination()
        await channel.send("Here is your help, enjoy!")


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f"cogs.{filename[:-3]}")
        # bot.add_cog(f"cogs.{filename[:-3]}")
#
# bot.add_cog(levels.Levelsys(bot))
# bot.add_cog(wanted.WantedUser(bot))
bot.run(settings.token)
