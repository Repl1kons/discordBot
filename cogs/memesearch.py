import json

import discord
from pydoc import cli
from discord.ext import commands
import urllib
import random

class Search_meme(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="Meme", help="Search meme on the reddit", aliases=["meme"])
    async def meme(self, ctx):
        memeApi = urllib.request.urlopen('https://meme-api.herokuapp.com/gimme')

        memeData = json.load(memeApi)

        memeUrl = memeData['url']
        memeName = memeData['title']
        memePoster = memeData['author']
        memeSub = memeData['subreddit']
        memelink = memeData['postLink']

        embed = discord.Embed(title=memeName, colour=discord.Colour.orange())
        embed.set_image(url = memeUrl)
        embed.set_footer(text=f"meme by: {memePoster} \n Subreddit: {memeSub} \n Post: {memelink}")

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Search_meme(bot))