import discord
from discord.ext import commands


class get_mute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="Mute",
                      help="Mute people (Only admin",
                      aliases=["mute"])
    @commands.has_role('Admin')
    async def mute(self, ctx, member: discord.Member, *, reason="Матерился"):
        guild = ctx.guild
        mutedrole = discord.utils.get(guild.roles, name="Muted")
        emb = discord.Embed(
            title=f"Muted по причине: {reason}",
            colour=discord.Colour.green())
        emb.set_author(name=member.name, icon_url=member.avatar_url)
        emb.add_field(name="Muted", value=f"Mute user {member.mention}")
        emb.set_footer(
            text='Был наказан администратором {}'.format(
                ctx.author.name),
            icon_url=ctx.author.avatar_url)

        if not mutedrole:
            mutedrole = await guild.create_role(name="Muted")

            for ch in guild.channels:
                await ch.set_permissions(mutedrole, speak=False, send_messages=False, read_message_history=True,
                                         read_messages=True)

        await member.add_roles(mutedrole, reason=reason)
        await ctx.send(embed=emb)
        await member.send(embed=emb)

    @commands.command(name="Unmute",
                      help="Unmute people (Only admin",
                      aliases=["unmute"])
    @commands.has_role('Admin')
    async def unmute(self, ctx, member: discord.Member):
        emb = discord.Embed(title=f"Unmuted", colour=discord.Colour.green())
        emb.set_author(name=member.name, icon_url=member.avatar_url)
        emb.add_field(name="Unmute", value=f"Unmute user {member.mention}")
        emb.set_footer(
            text='Был помилован администратором {}'.format(
                ctx.author.name),
            icon_url=ctx.author.avatar_url)

        emb1 = discord.Embed(title=f"Unmuted", colour=discord.Colour.green())
        emb1.set_author(name=member.name, icon_url=member.avatar_url)
        emb1.add_field(
            name=f"Unmute на сервере: {ctx.guild.name}",
            value=f"Unmute user {member.mention}")
        emb1.set_footer(
            text='Был помилован администратором {}'.format(
                ctx.author.name),
            icon_url=ctx.author.avatar_url)

        mutedrole = discord.utils.get(ctx.guild.roles, name="Muted")
        await member.remove_roles(mutedrole)
        await ctx.send(embed=emb)
        await member.send(embed=emb1)


def setup(client):
    client.add_cog(get_mute(client))
