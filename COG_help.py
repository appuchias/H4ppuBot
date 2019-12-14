import discord
from discord.ext import commands
from disputils import BotEmbedPaginator
import log

color = 0x7289DA

class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, ctx):
        page1 = discord.Embed(title="~General~", descrription='**Comandos generales**', color=color)
        page2 = discord.Embed(title="~Chat~", description="**Comandos con respuestas en el chat directas**", color=color)
        page3 = discord.Embed(title="~Custom~", description="**Comandos de tareas muy concretas**", color=color)
        page4 = discord.Embed(title="~Extensions~", description="**Comandos de manejo de extensiones**", color=color)
        page5 = discord.Embed(title="~Mod~", description="**Comandos de moderación** [Solo Mods]", color=color)

        page1.add_field(name='***help**', value='Muestra este comando', inline=False)

        page2.add_field(name='***suma <n>**', value='Suma los números que le pases.', inline=False)
        page2.add_field(name='***ping**', value='Responde Pong! Usado para medir la latencia', inline=False)
        page2.add_field(name='***di <msg>***', value='Dice lo que pongas.', inline=False)
        page2.add_field(name='***reverse <msg>**', value='Dice al revés lo que pone.', inline=False)
        page2.add_field(name='***hello**', value='World!', inline=False)
        page2.add_field(name='***repite <veces> <msg>**', value='Repite lo que quieras hasta 10 veces.', inline=False)
        page2.add_field(name='***dado <n de caras>**', value='Tira un dado de cualquier número de caras.', inline=False)
        page2.add_field(name='***moneda [n]**', value='Lanza una moneda n veces (1 por defecto).', inline=False)

        page3.add_field(name='***private**', value='Crea un canal de voz privado para ti. (No spamear <#641041860294606915>) [Solo en <#642856275104759809>]', inline=False)

        page4.add_field(name="***load <Extensión>**", value="Carga la extensión que le digas [Solo Mods]", inline=False)
        page4.add_field(name="***unload <Extensión>**", value="Descarga la extensión que le digas [Solo Mods]", inline=False)
        page4.add_field(name="***reload <Extensión>**", value="Recarga la extensión que le digas [Solo Mods]", inline=False)

        page4.add_field(name='***clear <n>**', value='Elimina hasta 20 mensajes', inline=False)
        page4.add_field(name='***kick <@member> [motivo]**', value='Echa a alguien', inline=False)
        page4.add_field(name='***ban <@member> [motivo]**', value='Banea a alguien', inline=False)

        page4.add_field(name='***warn <@member> [motivo]**', value="Avisa a alguien. Especifica motivo por favor", inline=False)
        page4.add_field(name='***mute <@member>**', value="Mutea a alguien", inline=False)
        page4.add_field(name='***tmute <@member> <tiempo(minutos)>**', value="Mutea a alguien durante el tiempo que le digas", inline=False)

        page5.add_field(name='`~Mod~`', value='**Comandos de moderación** [Solo Mods]', inline=False)
        page5.add_field(name='***clear <n>**', value='Elimina hasta 20 mensajes', inline=False)
        page5.add_field(name='***kick <@member> [motivo]**', value='Echa a alguien', inline=False)
        page5.add_field(name='***ban <@member> [motivo]**', value='Banea a alguien', inline=False)

        page5.add_field(name='***warn <@member> [motivo]**', value="Avisa a alguien. Especifica motivo por favor", inline=False)
        page5.add_field(name='***mute <@member>**', value="Mutea a alguien", inline=False)
        page5.add_field(name='***tmute <@member> <tiempo(minutos)>**', value="Mutea a alguien durante el tiempo que le digas", inline=False)

        embeds = [page1, page2, page3, page4, page5]

        paginator = BotEmbedPaginator(ctx, embeds)
        await paginator.run()

        await log.log(ctx, f"Help {ctx.author}")

def setup(client):
    client.add_cog(Help(client))