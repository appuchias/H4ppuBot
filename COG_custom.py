import discord
from discord.ext import commands, tasks
import log

users = {}

class Custom(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener(name="on_message")
    async def msg_receieved(self, message):
        if message.embeds or message.author == self.client.user or message.author.bot:
            return
        if message.channel.id == 641041861800362014:
            ayuda = await self.client.fetch_channel(641041861800362014)
            appu = message.guild.get_member(455321214525767680)
            await ayuda.send(f"{appu.mention}, {message.author.name} ha pedido ayuda!\n{message.content}")
            await message.delete(delay=2)
        if "hello" in message.content[:5]:
            await message.channel.send("world! :earth_africa:")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        channel = self.client.get_channel(payload.channel_id)
        msg = await channel.fetch_message(payload.message_id)
        notif = discord.utils.get(msg.guild.roles, name="Notif")
        userid = payload.user_id

        if payload.emoji.name == "✅": # El emoji de la reacción
            if channel.id == 641041859619323918 or channel.id == 641041860294606915: # Para evitar falsos positivos y que se añadan personas que no corresponden
                if not userid in users: # Para evitar errores de inexistencia
                    users[userid] = 0
                users[userid] += 1 # Para que conste que ha reaccionado
                await log.log(channel, f"{msg.author} reacted, {users.get(userid)}/2 done!") # Necesario en las primeras implementaciones

                if users.get(userid) == 2: # Si ya ha reaccionado en los 2 canales
                    del users[userid] # Restrinjo el diccionario a la gente que quede a medias para evitar lag en un futuro
                    readme = discord.utils.get(msg.guild.roles, name="Readme")
                    todos = discord.utils.get(msg.guild.roles, name="Todos")
                    await msg.author.remove_roles(readme) # Para que tengan acceso al resto del servidor
                    await msg.author.add_roles(todos)     # ^

        elif payload.emoji.id == 657718546511691797 and msg.id == 651910183752171567:
            await msg.author.add_roles(notif)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload): # Por si alguien elimina una de sus reacciones y no había mandado las 2
        channel = self.client.get_channel(payload.channel_id)
        msg = await channel.fetch_message(payload.message_id)
        notif = discord.utils.get(msg.guild.roles, name="Notif")
        if payload.emoji.name == "✅":
            if channel.id == 641041859619323918 or channel.id == 641041860294606915:
                if payload.user_id in users:
                    users[payload.user_id] -= 1

        elif payload.emoji.id == 657718546511691797 and msg.id == 651910183752171567:
            await msg.author.remove_roles(notif)

    @commands.command()
    async def private(self, ctx, *, name):
        if ctx.channel.id == 642856275104759809:
            mine = discord.utils.get(ctx.guild.voice_channels, id=641041878854139945)
            new = await mine.clone(name=name)
            await new.set_permissions(ctx.author, read_messages=True, connect=True)
            await new.set_permissions(ctx.guild.default_role, read_messages=False, connect=False)
        else:
            try:
                await ctx.author.send("Envía el mensaje en el canal correcto! :confused:")
            except:
                pass
        await ctx.message.delete(delay=1)
        await log.log(ctx, f"Private channel {name} created by {ctx.author}")

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


    @tasks.loop(seconds=10)
    async def members_update(self):
        channel = await self.client.fetch_channel(645312760598495253)
        members = 0
        for member in channel.guild.members:
            if not member.bot:
                members += 1
        await channel.edit(name=f"Miembros humanos: {members}", reason="Member update")

def setup(client):
    client.add_cog(Custom(client))
