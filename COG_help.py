import discord
from discord.ext import commands
from disputils import BotEmbedPaginator
import log
from datetime import datetime as dt
import pytz

color = 0x7289DA
tz = pytz.timezone("Europe/Madrid")

class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group()
    async def help(self, ctx):
        if ctx.invoked_subcommand is None:
            timestamp = dt.fromtimestamp(dt.timestamp(dt.now(tz=tz)))
            page1 = discord.Embed(title="~General~", descrription='**Comandos generales**', color=color, timestamp=timestamp)
            page2 = discord.Embed(title="~Chat~", description="**Comandos con respuestas en el chat directas**", color=color, timestamp=timestamp)
            page3 = discord.Embed(title="~Custom~", description="**Comandos de tareas muy concretas**", color=color, timestamp=timestamp)
            page4 = discord.Embed(title="~Extensions~", description="**Comandos de manejo de extensiones**", color=color, timestamp=timestamp)
            page5 = discord.Embed(title="~RRSS~", description="**Comandos de redes sociales**", color=color, timestamp=timestamp)
            page6 = discord.Embed(title="~Mod~", description="**Comandos de moderación** [Solo Mods]", color=color, timestamp=timestamp)

            page1.add_field(name='***help**', value='Muestra este comando', inline=False)

            page2.add_field(name='***suma <n>**', value='Suma los números que le pases.', inline=False)
            page2.add_field(name='***ping**', value='Responde Pong! Usado para medir la latencia', inline=False)
            page2.add_field(name='***di <msg>***', value='Dice lo que pongas.', inline=False)
            page2.add_field(name='***reverse <msg>**', value='Dice al revés lo que pone.', inline=False)
            page2.add_field(name='***hello**', value='World!', inline=False)
            page2.add_field(name='***repite <veces> <msg>**', value='Repite lo que quieras hasta 10 veces.', inline=False)
            page2.add_field(name='***dado <n de caras>**', value='Tira un dado de cualquier número de caras.', inline=False)
            page2.add_field(name='***moneda [n]**', value='Lanza una moneda n veces (1 por defecto).', inline=False)

            page3.add_field(name='***private**', value='Crea un canal de voz privado para ti. (No spamear, leed <#641041860294606915>) [Solo permitido en <#642856275104759809>]', inline=False)

            page4.add_field(name="***load <Extensión>**", value="Carga la extensión que le digas [Solo Mods]", inline=False)
            page4.add_field(name="***unload <Extensión>**", value="Descarga la extensión que le digas [Solo Mods]", inline=False)
            page4.add_field(name="***reload <Extensión>**", value="Recarga la extensión que le digas [Solo Mods]", inline=False)

            page5.add_field(name="***insta <cuenta>**", value="Muestra la última foto de una cuenta pública, junto a sus likes y comentarios", inline=False)
            page5.add_field(name="***twitter <cuenta>**", value="Responde con los 10 últimos tweets de una cuenta", inline=False)
            page5.add_field(name="***reddit <subreddit>**", value="Manda un mensaje con los 10 últimos posts del subreddit", inline=False)

            page6.add_field(name='***clear <n>**', value='Elimina hasta 20 mensajes', inline=False)
            page6.add_field(name='***kick <@member> [motivo]**', value='Echa a alguien', inline=False)
            page6.add_field(name='***ban <@member> [motivo]**', value='Banea a alguien', inline=False)
            page6.add_field(name='***warn <subcomando>**', value="Inútil sin subcomando mencionado `*help warn` para más info", inline=False)
            page6.add_field(name='***mute <@member>**', value="Mutea a alguien", inline=False)

            embeds = [page1, page2, page3, page4, page5, page6]

            paginator = BotEmbedPaginator(ctx, embeds)
            await paginator.run()

            await log.log(ctx, f"Help {ctx.author}")
    
    @help.command()
    async def warn(self, ctx):
        timestamp = dt.fromtimestamp(dt.timestamp(dt.now(tz=tz)))
        embed = discord.Embed(title="~Warn~", descrription='**Subcomandos**', color=color, timestamp=timestamp)
        embed.add_field(name="user <usuario> [motivo]", value="Manda un aviso a un miembro del servidor", inline=False)
        embed.add_field(name="claim [motivo]", value="Reclama tu último aviso", inline=False)
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Help(client))
