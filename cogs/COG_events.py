import discord
from discord.ext import commands
import asyncio
import log

#Bot prefix
prefix = '*'

class Events(commands.Cog):
    def __init__(self, client):
        self.client = client

    #Events
    @commands.Cog.listener(name="on_message")
    async def on_msg(self, message):
        if message.embeds or message.author == self.client.user or message.author.bot:
            return
        else:
            await log.log(message, f'(#{message.channel}) ${message.author}: {message.content.replace("@", "$")}')

    # #When a reaction is added to a message
    # @commands.Cog.listener()
    # async def on_reaction_add(self, reaction, user):
    #     await log.log(reaction.message.channel, f'(#{reaction.message.channel}): Reacción {str(reaction)} añadida al mensaje "{reaction.message.content}" por {user}')

    # #When a reaction is removed from a message
    # @commands.Cog.listener()
    # async def on_reaction_remove(self, reaction, user):
    #     await log.log(reaction.message.channel, f'(#{reaction.message.channel}): Reacción {str(reaction)} eliminada del mensaje "{reaction.message.content}" por {user}')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        new = discord.utils.get(member.guild.roles, name="Readme")
        await member.add_roles(new)
        await member.send(f"Bienvenido al server **{member.guild}**!")
        channel = discord.utils.get(member.guild.channels, name="usuarios")
        await channel.send(f"{member.mention} se acaba de unir! :tada:")
        await log.log(member, f"{member.mention} se acaba de unir! :tada:")

    @commands.Cog.listener()
    async def on_member_remove(self,member):
        user = member
        channel = discord.utils.get(member.guild.channels, name="usuarios")
        await channel.send(f"{user} se acaba de ir, parece que no lo pasaba bien D:")
        await log.log(member, f"{user} se acaba de ir, parece que no lo pasaba bien D:")

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
    client.add_cog(Events(client))
