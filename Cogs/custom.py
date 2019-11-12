import discord
from discord.ext import commands, tasks
import asyncio

class Custom(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener(name="on_message")
    async def msg_receieved(self, message):
        if message.embeds or message.author == self.client.user or message.author.bot or message.channel.id == 637356734649729044:
            return
        else:
            if message.channel.id == 637356732137603092:
                ayuda = discord.utils.get(message.guild.channels, name="help")
                await ayuda.send(f"<@641041849997328384>, {message.author} ha pedido ayuda!\n{message.content}")
                await asyncio.sleep(2)
                await message.remove()

    @commands.command()
    async def private(self, ctx, *, name):
        if ctx.channel.id == 642856275104759809:
            mine = discord.utils.get(ctx.guild.voice_channels, id=641041878854139945)
            new = await mine.clone(name=name)
            #new = discord.utils.get(message.guild.voice_channels, name=name)
            await new.set_permissions(ctx.author, connect=True)
            await new.set_permissions(ctx.guild.default_role, connect=False)
        else:
            await ctx.author.send("Envía el mensaje en el canal correcto! :confused:")

def setup(client):
    client.add_cog(Custom(client))
