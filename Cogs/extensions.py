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
        await asyncio.sleep(2)
        self.client.load_extension(f'Cogs.{extension}')
        await ctx.send(f'Extensión {extension} recragada!')
        await self.log(ctx, f'Extension {extension} reloaded!')

    #Logging function
    async def log(self, ctx, msg):
        channel = discord.utils.get(ctx.guild.channels, name='log')
        if channel in ctx.guild.channels:
            pass
        else:
            await ctx.guild.create_text_channel(name='log', topic="El log del bot. Silénciame si no quieres morir por notificaciones :)", reason='Log necesario...')
            channel = discord.utils.get(ctx.guild.channels, name='log')
            overwrites = {ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False)}

            top_two = ctx.guild.roles[-2:]
            for role in top_two:
                overwrites[role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
        await channel.send(msg)
        print(f"Log: {msg}")

        with open("modlog.txt", "a") as f:
            f.write(f"Log: {msg}\n")

def setup(client):
    client.add_cog(Extensions(client))
