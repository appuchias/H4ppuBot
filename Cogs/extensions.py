import discord
from discord.ext import commands
import asyncio

prefix = '*'

class Extensions(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.client.log = self.log

    #Commands
    #Load an extension
    @commands.command()
    async def load(self, ctx, extension):
        self.client.load_extension(f'Cogs.{extension}')
        await ctx.send(f'Extensión {extension} cargada!')
        await self.log(ctx, f'Extension {extension} loaded!')

    #Unload an extension
    @commands.command()
    async def unload(self, ctx, extension):
        self.client.unload_extension(f'Cogs.{extension}')
        await ctx.send(f'Extensión {extension} descargada!')
        await self.log(ctx, f'Extension {extension} unloaded!')

    #Reload an extension
    @commands.command()
    async def reload(self, ctx, extension):
        self.client.unload_extension(f'Cogs.{extension}')
        await ctx.send(f'Extension {extension} descargada!')
        await ctx.send('Recargando en breve...')
        await asyncio.sleep(1)
        self.client.load_extension(f'Cogs.{extension}')
        await ctx.send(f'Extensión {extension} recragada!')
        await self.log(ctx, f'Extension {extension} reloaded!')

    #Log
    async def log(self, ctx, msg):
        channel = self.client.fetch_channel(641041858012905480)
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
    client.add_cog(Extensions(client))
