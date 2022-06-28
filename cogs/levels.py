import discord
import json

from discord import File
from discord.ext import commands
from typing import Optional
from easy_pil import Editor, load_image_async, Font


level = ["Level-5+", "Level-10+", "Level-15+"]


level_num = [5, 10, 15]


class Levelsys(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Leveling Cog Ready!")

    # this will increase the user's xp everytime they message
    @commands.Cog.listener()
    async def on_message(self, message):


        if not message.content.startswith("/"):

            # checking if the bot has not sent the message
            if not message.author.bot:
                with open("levels.json", "r") as f:
                    data = json.load(f)

                # checking if the user's data is already there in the file or not
                if str(message.guild.id) in data:
                    if str(message.author.id) in data[str(message.guild.id)]:
                        xp = data[str(message.guild.id)][str(message.author.id)]['xp']
                        lvl = data[str(message.guild.id)][str(message.author.id)]['level']

                        # increase the xp by the number which has 100 as its multiple
                        increased_xp = xp + 25
                        new_level = int(increased_xp / 100)

                        data[str(message.guild.id)][str(message.author.id)]['xp'] = increased_xp

                        with open("levels.json", "w") as f:
                            json.dump(data, f)

                        if new_level > lvl:
                            await message.channel.send(
                                f"{message.author.mention} Только что получил новый уровень: {new_level}!!!")

                            data[str(message.guild.id)][str(message.author.id)]['level'] = new_level
                            data[str(message.guild.id)][str(message.author.id)]['xp'] = 0

                            with open("levels.json", "w") as f:
                                json.dump(data, f)

                            for i in range(len(level)):
                                if new_level == level_num[i]:
                                    await message.author.add_roles(
                                        discord.utils.get(message.author.guild.roles, name=level[i]))

                                    mbed = discord.Embed(title=f"{message.author} Получил новую роль **{level[i]}**!",
                                                         color=message.author.colour)
                                    mbed.set_thumbnail(url=message.author.avatar_url)
                                    await message.channel.send(embed=mbed)
                        return

                if str(message.guild.id) in data:
                    data[str(message.guild.id)][str(message.author.id)] = {}
                    data[str(message.guild.id)][str(message.author.id)]['xp'] = 0
                    data[str(message.guild.id)][str(message.author.id)]['level'] = 1
                else:
                    data[str(message.guild.id)] = {}
                    data[str(message.guild.id)][str(message.author.id)] = {}
                    data[str(message.guild.id)][str(message.author.id)]['xp'] = 0
                    data[str(message.guild.id)][str(message.author.id)]['level'] = 1

                with open("levels.json", "w") as f:
                    json.dump(data, f)


    @commands.command(name="Rank", help="View you progress on the server", aliases=["rank"])
    async def rank(self, ctx: commands.Context, user: Optional[discord.Member]):
        userr = user or ctx.author

        with open("levels.json", "r") as f:
            data = json.load(f)

        # with open("userdata.json", "r") as f:
        #     user_data = json.load(f)

        xp = data[str(ctx.guild.id)][str(userr.id)]["xp"]
        lvl = data[str(ctx.guild.id)][str(userr.id)]["level"]

        next_level_xp = (lvl + 1) * 100
        xp_need = next_level_xp
        xp_have = data[str(ctx.guild.id)][str(userr.id)]["xp"]

        percentage = int(((xp_have * 100) / xp_need))

        if percentage < 1:
            percentage = 0

        ## Rank card
        background = Editor(f"cogs/images/zIMAGE.png")
        profile = await load_image_async(str(userr.avatar_url))

        profile = Editor(profile).resize((150, 150)).circle_image()

        poppins = Font.poppins(size=40)
        poppins_small = Font.poppins(size=30)


        ima = Editor("cogs/images/zBLACK.png")
        background.blend(image=ima, alpha=.5, on_top=False)

        background.paste(profile.image, (30, 30))

        background.rectangle((30, 220), width=650, height=40, fill="#fff", radius=20)
        background.bar(
            (30, 220),
            max_width=650,
            height=40,
            percentage=percentage,
            fill="#ff9933",
            radius=20,
        )
        background.text((200, 40), str(userr.name), font=poppins, color="#ff9933")

        background.rectangle((200, 100), width=350, height=2, fill="#ff9933")
        background.text(
            (200, 130),
            f"Level : {lvl}   "
            + f" XP : {xp} / {(lvl + 1) * 100}",
            font=poppins_small,
            color="#ff9933",
        )

        card = File(fp=background.image_bytes, filename="cogs/images/zCARD.png")
        await ctx.send(file=card)

    @commands.command(name="Leader", help="View leader-board on the server", aliases=["leader"])
    async def leaderboard(self, ctx, range_num=5):
        with open("levels.json", "r") as f:
            data = json.load(f)

        l = {}
        total_xp = []

        for userid in data[str(ctx.guild.id)]:
            xp = int(
                data[str(ctx.guild.id)][str(userid)]['xp'] + (int(data[str(ctx.guild.id)][str(userid)]['level']) * 100))

            l[
                xp] = f"{userid};{data[str(ctx.guild.id)][str(userid)]['level']};{data[str(ctx.guild.id)][str(userid)]['xp']}"
            total_xp.append(xp)

        total_xp = sorted(total_xp, reverse=True)
        index = 1
        file_title = discord.File("cogs/images/images.png", filename="images.png")

        mbed = discord.Embed(
            title="Leaderboard"
        )

        mbed.set_thumbnail(url="attachment://images.png")

        for amt in total_xp:
            id_ = int(str(l[amt]).split(";")[0])
            level = int(str(l[amt]).split(";")[1])
            xp = int(str(l[amt]).split(";")[2])

            member = await self.bot.fetch_user(id_)

            if member is not None:
                name = member.name
                mbed.add_field(name=f"{index}. {name}",
                               value=f"**Level: {level} | XP: {xp}**",
                               inline=False)

                if index == range_num:
                    break
                else:
                    index += 1

        await ctx.send(file=file_title, embed=mbed)

    @commands.command("Rank_reset", help="Reset rank user (Only admin)", aliases=["rank_reset"])
    @commands.has_role('Admin')
    async def rank_reset(self, ctx, user: Optional[discord.Member]):
        member = user or ctx.author

        if not member == ctx.author:
            role = discord.utils.get(ctx.author.guild.roles, name="Bot-Mod")

            if not role in member.roles:
                await ctx.send(f"Вы можете сбросить только свои данные, для сброса других данных необходимо иметь роль {role.mention}")
                return

        with open("levels.json", "r") as f:
            data = json.load(f)

        del data[str(ctx.guild.id)][str(member.id)]

        with open("levels.json", "w") as f:
            json.dump(data, f)

        await ctx.send(f"{member.mention}'s Уровни сброшены")




def setup(client):
    client.add_cog(Levelsys(client))