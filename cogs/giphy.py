import discord
from discord.ext import commands
import giphy_client
from giphy_client.rest import ApiException
import random

class giphy(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="Gif", help="Search gif", aliases=["gif"])
    async def gif(self, ctx, *, q="Smile"):
        api_key = "Opz9aNd9n5kE2Ud4dMMe0l5Ge9jYgMfv"
        api_instance = giphy_client.DefaultApi()

        try:
            api_responce = api_instance.gifs_search_get(api_key, q, limit=5, rating='g')
            lst = list(api_responce.data)
            giff = random.choice(lst)

            embed = discord.Embed(title=f"Search gif: {q}")
            embed.set_image(url=f"https://media.giphy.com/media/{giff.id}/giphy.gif")

            await ctx.send(embed=embed)

        except ApiException as r:
            print("Exception for the api")


def setup(bot):
    bot.add_cog(giphy(bot))