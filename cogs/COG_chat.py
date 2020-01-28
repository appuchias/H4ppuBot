import discord
from discord.ext import commands
import random
import log

class Chat(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.command()
    async def suma(self, ctx, args: commands.Greedy[int]):
        output=0
        for n in args:
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

        if veces <= 10:
            embed = discord.Embed(title=f"**{self.client.user.name}**", description='Repite "{}" {} veces'.format(output, veces), colour=0x7289DA)
            for i in range(veces):
                embed.add_field(name=f'Repetición {i} de {veces}', value=output, inline=True)
            await ctx.send(embed=embed)
        else:
            await ctx.send('Me da bastante pereza tantas veces, es muy repetitivo. Me empiezo a cansar a partir de 10')

    @commands.command()
    async def dado(self, ctx, n):
        number = random.randint(1,int(n))
        await ctx.send(number)
        await log.log(ctx, f"Dado: {number}")

    @commands.command()
    async def moneda(self, ctx, repetitions:int=1):
        if repetitions > 0 and repetitions <= 20:
            embed = discord.Embed(title="Moneda", description=f"{repetitions} repeticiones", colour=0xf1c40f)
            for cnt in range(repetitions):
                n = random.randint(0, 181)
                if n <= 90:
                    embed.add_field(name=f"{cnt+1}/{repetitions}", value="CARA! :adult:")
                elif n < 181:
                    embed.add_field(name=f"{cnt+1}/{repetitions}", value="CRUZ! :x:")
                else:
                    embed.add_field(name=f"{cnt+1}/{repetitions}", value="CANTOOOOO!!! :tada::tada:")
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
