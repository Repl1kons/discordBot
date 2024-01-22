import discord
from discord.ext import commands
import main


class Message(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(status=discord.Status.online, activity=discord.Game(""))

    @commands.command(name="Create_rule",
                      help="Clear rule (Only admin)",
                      aliases=["create_rule"])
    async def rule(self, ctx):
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name="Rule")
        embed.add_field(name="Правило 1: ", value="Админ всегда прав")
        embed.add_field(
            name="Правило 2: ",
            value="Если ты думаешь что админ не прав то ты непра\
                                                    вильно думаешь, смотри правило 1")

        embed.add_field(name="Правило 3: ", value="Админу все должны платить,\
                                                    если ты не хочешь этого делать то смотри правило 2")
        embed.add_field(
            name="Правило 4: ",
            value="Админ может все, независимо от тебя")
        embed.set_image(
            url="https://media.discordapp.net/attachments/854683737895337987/856133698688122890/unknown.png?width=719"
                "&height=406")

        await ctx.send(embed=embed)

    @commands.command(name="Clear",
                      help="Clear messages on chat (Only admin)",
                      aliases=["clear"])
    @commands.has_role('Admin')
    async def clear(self, ctx, amount=1000):
        await ctx.channel.purge(limit=amount)
        emb = discord.Embed(title="Очищено", colour=discord.Colour.green())
        emb.add_field(
            name="Бот:",
            value=f"Сообщения в канале {ctx.guild.name} были очищены")
        emb.set_footer(
            text='Чат был очищен по просьбе администратора {}'.format(
                ctx.author.name),
            icon_url=ctx.author.avatar_url)
        await ctx.send(embed=emb)

    @commands.Cog.listener()
    async def on_command_error(self, error):
        print(f"Произошла ошибка: {error}")

    @commands.command(name="Help", aliases=["help"])
    async def help(self, ctx):
        # file_title = discord.File("cogs/images.png", filename="images.png")
        embed = discord.Embed(
            title=f'Навигация по командам\nCommand prefix - [ {main.bot.command_prefix} ]',
            colour=discord.Colour.blue())

        embed.add_field(
            name='Clwarn',
            value='очистка базы данных от предупреждений мата (только для админов)')
        embed.add_field(
            name='Status',
            value='Просмотр статуса своих предупреждений мата')
        embed.add_field(
            name='Rank',
            value='Просмотр прогресса активности на сервере')
        embed.add_field(
            name='Leader',
            value="Просмотр самых активных пользователей")
        embed.add_field(
            name='Rank_reset',
            value='Очистка статистики активности пользователей на сервере\
         (только для админов)')
        embed.add_field(name='Clear', value='Очистка сообщений в канале')
        embed.add_field(
            name='Play',
            value='Проигрывание музыки в голос. канале | /play [название/ссылка на трек] ')
        embed.add_field(name='Pause', value='Пауза трека')
        embed.add_field(
            name='Resume',
            value='Продолжение воспроизведения трека')
        embed.add_field(name='NowPlaying', value='Сейчас играет:')
        embed.add_field(name='Loop', value='Зациклить трек')
        embed.add_field(name='Stop', value='Закончить воспроизведения трека')
        embed.add_field(
            name='Join_play | or | join',
            value='Бот присоединяется к каналу, на котором находится автор | '
            'необязательно, можно использовать /play')
        embed.add_field(
            name='Skip',
            value='Переход к следующему треку из очереди')
        embed.add_field(name='Leave', value='Выход бота из голос. канала')
        embed.add_field(name='Queue', value='Просмотр очереди треков')
        embed.add_field(name='ClearQueue', value='Очистка очереди треков')
        embed.add_field(
            name='Remove',
            value='Удаление трека из очереди | /remove [число позиции трека в очереди]')
        embed.add_field(name='Meme', value='Показ мемов')
        embed.add_field(
            name='Join_voice',
            value='Вы можете быстро подключиться к голосовому каналу друга без поиска '
            'его | для этого надо зайти в любой голос. канал и написать эту '
            'команду')
        embed.add_field(
            name='Report',
            value='Отправление жалобы на пользователя | /report [@пользователь]')
        embed.add_field(
            name='Mute',
            value='Мут пользователя (только для админов)')
        embed.add_field(
            name='Unmute',
            value='Размут пользователя (только для админов)')
        embed.add_field(
            name='Gif',
            value='Поиск гиф-видео | /gif[слово для поиска]')
        embed.add_field(
            name='Weather',
            value='Показ погоды в городе | /weather [Город]')
        embed.add_field(
            name='Wanted',
            value='Поиск пользователя на сервере | /wanted[@пользователь]')
        embed.add_field(
            name='Help',
            value='Показ и обьяснение команд которые умеет бот')
        embed.set_footer(
            text="Создатель бота: Garnlzerx#0738",
            icon_url="https://sun9-6.userapi.com/impg"
            "/tRPGI8ZR0Gh7fFN5h8cjs5t0vT4zTAz-qiw0kg"
            "/Eepg2_BBwTM.jpg?size=719x713&quality=96"
            "&sign=e3bc486cbb14445c31898ce1ad27c71f&type"
            "=album")

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Message(bot))
