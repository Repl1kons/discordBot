import os
import discord
from discord.ext import commands
from extenshions.program import settings

bot = commands.Bot(command_prefix='/', intents=discord.Intents.all())
bot.remove_command("help")

class MyHelp(commands.HelpCommand):
    """My very own help formatter"""

    async def send_bot_help(self, mapping):
        """Send this on [p]help without arguments"""
        channel = self.get_destination()
        await channel.send("Here is your help, enjoy!")


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f"cogs.{filename[:-3]}")



bot.run(settings.token)
