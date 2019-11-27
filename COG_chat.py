import discord
from discord.ext import commands
import random
import log

class Chat(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.command()
    async def suma(self, ctx, *, args):
        output=0
        for n in args.split(" "):
            output+=int(n)
            print(output)
        await ctx.send(output)
        await log.log(ctx, output)

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"Pong! ||({round(self.client.latency*1000)}ms)||")
        await log.log(ctx, f"Pong! ||({round(self.client.latency*1000)}ms)||")

    @commands.command()
    async def di(self, ctx, *, args):
        output = ' '
        for word in args.split(" "):
            output += word
            output += ' '
        await ctx.send(output)
        await log.log(ctx, output)

    @commands.command()
    async def reverse(self, ctx, *, args):
        output = ' '
        for word in args.split(" "):
            output += word
            output += ' '
        output = output[::-1]
        await ctx.send(output)
        await log.log(ctx, f"Reverse: {output}")

    @commands.command()
    async def hello(self, ctx):
        await ctx.send("world! :earth_africa:")

    @commands.command()
    async def repite(self, ctx, veces:int, *args):
        output = ' '
        for word in args:
            output += word
            output += ' '

        embed = discord.Embed(
        title = f"**{self.client.user.name}**",
        description = 'Repite "{}" {} veces'.format(output, veces),
        colour = 0x7289DA
        )

        if veces <= 10:
            for i in range(veces):
                embed.add_field(name=output, value=f'Repetición {i} de {veces}', inline=False)
        else:
            await ctx.send('Me da bastante pereza tantas veces, es muy repetitivo. Me empiezo a cansar a partir de 10')
            await ctx.send(embed=embed)

    @commands.command()
    async def dado(self, ctx, n):
        number = random.randint(1,int(n))
        await ctx.send(number)
        await log.log(ctx, f"Dado: {number}")

    @commands.command()
    async def moneda(self, ctx, repetitions:int=1):
        embed = discord.Embed(title="", description="", colour=discord.Color.gold)
        if repetitions > 0 and repetitions <= 20:
            for cnt in range(1, repetitions+1):
                n = random.randint(0, 81)
                if n < 40:
                    embed.add_field(name=f"Repetición {cnt} de {repetitions}", value="CARA! :adult:")
                elif n < 81:
                    embed.add_field(name=f"Repetición {cnt} de {repetitions}", value="CRUZ! :x:")
                else:
                    embed.add_field(name=f"Repetición {cnt} de {repetitions}", value="CANTOOOOO!!! :tada::tada:")
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"Por favor, no te pases, {repetitions} está por encima de 20, mi máximo de repeticiones del comando! :warning:")

    #Log
    async def log(self, ctx, msg):
        channel = discord.utils.get(ctx.guild.text_channels, name="log")
        if channel in ctx.guild.text_channels:
            pass
        else:
            await ctx.send("Error 404. Channel not found")
            return

        await channel.send(msg)
        print(f"Log: {msg}")

        with open("modlog.txt", "a") as f:
            f.write(f"Log: {msg}\n")

def setup(client):
    client.add_cog(Chat(client))
