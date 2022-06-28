from discord.ext import commands
import discord

from discord import File
from discord.utils import get

from easy_pil import Editor, load_image_async, Font



class memberServ(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.intents = discord.Intents.default()
        self.intents.members = True

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot now online")

    @commands.Cog.listener()
    async def on_member_join(self, member):

        # add the channel id in which you want to send the card
        guilds = member.guild
        for guildname in guilds.channels:
            if guildname.name == "новые-пользователи":
                channel = self.bot.get_channel(guildname.id)
                memberole = discord.utils.get(guilds.roles, name="Member")

                # if you want to give any specific roles to any user then you can add like this
                if not memberole:
                    mutedrole = await guilds.create_role(name="Member")

                    for ch in guilds.channels:
                        await ch.set_permissions(mutedrole, speak=False, send_messages=False, read_message_history=True,
                                                 read_messages=True)

                await member.add_roles(memberole)
                # role = get(member.guild.roles, name="Member")
                # await member.add_roles(role)

                pos = sum(m.joined_at < member.joined_at for m in member.guild.members if m.joined_at is not None)

                if pos == 1:
                    te = "st"
                elif pos == 2:
                    te = "nd"
                elif pos == 3:
                    te = "rd"
                else:
                    te = "th"

                background = Editor("cogs/images/wlcbg.jpg")
                profile_image = await load_image_async(str(member.avatar_url))

                profile = Editor(profile_image).resize((150, 150)).circle_image()
                poppins = Font.poppins(size=50, variant="bold")

                poppins_small = Font.poppins(size=20, variant="light")

                background.paste(profile, (325, 90))
                background.ellipse((325, 90), 150, 150, outline="gold", stroke_width=4)

                background.text((400, 325), f"{member.name}#{member.discriminator}", color="white", font=poppins_small,
                                align="center")

                background.text((400, 260), f"WELCOME TO {member.guild.name}", color="white", font=poppins, align="center")

                background.text((400, 360), f"You Are The {pos}{te} Member", color="#0BE7F5", font=poppins_small,
                                align="center")

                file = File(fp=background.image_bytes, filename="wlcbg.jpg")

                # if you want to message more message then you can add like this
                await channel.send(
                    f"Heya {member.mention}! Welcome To **{member.guild.name}**")

                # for sending the card
                await channel.send(file=file)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        guild = member.guild
        for guildname in guild.channels:
            if guildname.name == "новые-пользователи":
                channel = self.bot.get_channel(guildname.id)

                await channel.send(f"{member.name} Has Left The server, We are going to miss you :( ")



def setup(client):
    client.add_cog(memberServ(client))