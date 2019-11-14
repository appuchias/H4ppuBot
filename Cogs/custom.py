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
                ayuda = self.client.fetch_channel(637356732137603092)
                await ayuda.send(f"<@641041849997328384>, {message.author} ha pedido ayuda!\n{message.content}")
                await message.delete(delay=2)

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
        await ctx.message.delete(delay=2)
        await self.log(ctx, f"Private channel {name} created by {ctx.author}")

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
    client.add_cog(Custom(client))
