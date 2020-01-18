import discord
from discord.ext import commands
import asyncio
import log

prefix = '*'

class Extensions(commands.Cog):
    def __init__(self, client):
        self.client = client

    #Commands
    #Load an extension
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def load(self, ctx, extension):
        self.client.load_extension(f'cogs.COG_{extension}')
        await ctx.send(f'Extensión {extension} cargada!')
        await log.log(ctx, f'Extension {extension} loaded!')

    #Unload an extension
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unload(self, ctx, extension):
        self.client.unload_extension(f'cogs.COG_{extension}')
        await ctx.send(f'Extensión {extension} descargada!')
        await log.log(ctx, f'Extension {extension} unloaded!')

    #Reload an extension
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def reload(self, ctx, extension):
        self.client.unload_extension(f'cogs.COG_{extension}')
        await ctx.send(f'Extension {extension} descargada!')
        await ctx.send('Recargando en breve...')
        await asyncio.sleep(1)
        self.client.load_extension(f'cogs.COG_{extension}')
        await ctx.send(f'Extensión {extension} recargada!')
        await log.log(ctx, f'Extension {extension} reloaded!')

def setup(client):
    client.add_cog(Extensions(client))
