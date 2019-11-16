import discord
from discord.ext import commands
import random

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
        await self.log(ctx, output)

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"Pong! ||({round(self.client.latency*1000)}ms)||")
        await self.log(ctx, f"Pong! ||({round(self.client.latency*1000)}ms)||")

    @commands.command()
    async def di(self, ctx, *, args):
        output = ' '
        for word in args.split(" "):
            output += word
            output += ' '
        await ctx.send(output)
        await self.log(ctx, output)

    @commands.command()
    async def reverse(self, ctx, *, args):
        output = ' '
        for word in args.split(" "):
            output += word
            output += ' '
        output = output[::-1]
        await ctx.send(output)
        await self.log(ctx, f"Reverse: {output}")

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
        colour = 0xf29fc5
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
        await self.log(ctx, f"Dado: {number}")

    @commands.command()
    async def moneda(self, ctx):
        n = random.randint(0, 81)
        if n < 40:
            await ctx.send("Ha salido cara! :adult:")
        elif n < 81:
            await ctx.send("Ha salido cruz! :x:")
        else:
            await ctx.send("Ha salido CANTO!! :tada::tada:")

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
