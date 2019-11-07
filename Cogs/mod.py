import discord
from discord.ext import commands
import asyncio
import json

class Mod(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.client.log = self.log

    #When a message is sent
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        else:
            await self.log(message, f'(#{message.channel}) ${message.author}: {message.content.replace("@", "$")}')
            user = message.author
            bad_words = ["puta", "puto", "gilipollas", "hijo de", "cabron", "cabrón", "pvta", "pvto", "pta", "pto", "p*to", "p*ta", "asshole"]
            for word in bad_words:
                if word in message.content.lower():
                    await self.warning(user, user, f"Used a bad word ({word})")
                    await self.log(user, f"{user} used a bad word ({word})")

    #Commands
    #Bulk message delete
    @commands.command()
    @commands.has_role("H4lppu")
    async def clear(self, ctx, number):
        n = number
        if int(n) > 20:
          await ctx.send('Demasiados mensajes para eliminar...')
          return
        await ctx.channel.purge(limit=(int(n)+1))
        await ctx.send(f'{str(n)} mensaje(s) eliminados!')
        print(f'{str(n)} messages cleared in #{ctx.channel.name}')
        await self.log(ctx, f'{str(n)} messages cleared in #{ctx.channel.name} by {ctx.message.author}')
        await ctx.message.delete(delay=2)

    #Kick someone
    @commands.command()
    @commands.has_role("H4lppu")
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f'{member} kickeado!')
        await self.log(ctx, f'{member} was kicked by {ctx.message.author}')
        await ctx.message.delete(delay=2)

    #Ban someone
    @commands.command()
    @commands.has_role("H4lppu")
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f'{member} baneado!')
        await self.log(ctx, f'{member} was banned by {ctx.message.author}')
        await ctx.message.delete(delay=2)

    #Unban someone
    @commands.command()
    @commands.has_role("H4lppu")
    async def unban(self, ctx, *, member):
        banned_users = ctx.guild.bans()
        name, discr = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user
            if(user.name, user.discriminator) == (name, discr):
                await ctx.guild.unban(user)
                await self.log(ctx, f'{user} was unbanned by {ctx.message.author}')
                return
        await ctx.send(f'{member} desbaneado!')
        await ctx.message.delete(delay=2)

    @commands.command()
    @commands.has_role("H4lppu")
    async def warn(self, ctx, user:discord.Member, *, reason = "None"):
        await self.warning(ctx, user, reason)
        await self.log(ctx, f"{ctx.author} warned {user.name}!")
        await ctx.send(f"{user.name} fue alertado por {ctx.author}")
        await ctx.message.delete(delay=2)


    @commands.command()
    @commands.has_role("H4lppu")
    async def mute(self, ctx, user: discord.Member):
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted role")
        await user.add_roles(muted_role)
        await self.log(ctx, f"{user.name} got muted!")

    @commands.command()
    @commands.has_role("H4lppu")
    async def tmute(self, ctx, user: discord.Member, n:int):
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted role")
        await user.add_roles(muted_role)
        await self.log(ctx, f"{user.name} got muted for {n}m!")
        await asyncio.sleep(n*60)
        await user.remove_roles(muted_role)

    @commands.command()
    @commands.has_role("H4lppu")
    async def report(self, ctx, who : discord.Member, *, reason):
        with open("reports.json", "r") as f:
        	reports = json.load(f)
        channel = discord.utils.get(ctx.guild.channels, name="reports")
        appu = discord.utils.get(ctx.guild.members, id=455321214525767680)
        if who.id in reports:
            reports[who.id] += 1
        else:
            reports[who.id] = 1
        await appu.send(f"{ctx.auhor.mention} reported {who.mention} for {reason} and now has {reports.get(who.id)} reports!")
        if reports.get(who.id) >= 3:
        	await appu.send(f"{appu.mention}, {who.name} has {reports.get(who.id)} reports!!!")
        await channel.send(f"""||-------------------------------------------------------------------------------------------||
Case **{len(reports)}**:\n - Member: **{who}**\n - Actual reports: **{reports.get(who.id)}**\n - Reason: *{reason}*""")
        with open ("reports.json", "w") as f:
            json.dump(reports, f, indent=4)

    #Función para poder añadir eventos al log
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

    #Warn function
    async def warning(self, ctx, user, reason):
        with open("warns.json", "r") as f:
            warns = json.load(f)

        if str(user.id) in warns:
            warns[str(user.id)] += 1
        else:
            warns[str(user.id)] = 1
        await user.send(f"Fuiste alertado por: {reason}\nTienes {warns[str(user.id)]} avisos. **Ten cuidado!**:warning:\n||Con 3 avisos: Muteo de 1h.\tCon 5 avisos: Muteo de 12h.\tCon 10 avisos: Expulsión.\tCon 15 avisos: Baneo permanente no revisable.\n*Los avisos se guardan aunque te vayas y vuelvas a entrar!*||")
        with open("warns.json", "w") as f:
            json.dump(warns, f, indent=4)

        if warns[str(user.id)] == 3:
            muted_role = discord.utils.get(ctx.guild.roles, name="Muted role")
            if muted_role in ctx.guild.roles:
                for channel in ctx.guild.channels:
                    await channel.set_permissions(muted_role, reason="Muted role",send_messages=False)
                await user.add_roles(muted_role)
                await self.log(ctx, f"Temp muted {user.name} for warning accumulation")
                await user.send(f"You got muted in **{ctx.guild.name}** for 1h for warning accumulation")
            else:
                muted_role = await ctx.guild.create_role(name="Muted role", permissions=discord.Permissions.none(), colour=discord.Color.dark_grey(), hoist=True)
                for channel in ctx.guild.channels:
                    await channel.set_permissions(muted_role, reason="Muted role",send_messages=False)
                for cnt in range(6):
                    try:
                        muted_role = discord.utils.get(ctx.guild.roles, name="Muted role")
                        await muted_role.edit(position=(len(ctx.guild.roles)-cnt))
                        print(1)
                    except:
                        pass
                await user.add_roles(muted_role)
                await self.log(ctx, f"Temp muted {user.name} for warning accumulation")
                await user.send(f"Muteado en **{ctx.guild.name}** durante 1h por acumulación de avisos")
            await asyncio.sleep(3600)
            await user.remove_roles(muted_role)
        elif warns[str(user.id)] == 5:
            muted_role = discord.utils.get(ctx.guild.roles, name="Muted role")
            if muted_role in ctx.guild.roles:
                for channel in ctx.guild.channels:
                    await channel.set_permissions(muted_role, reason="Muted role",send_messages=False)
                await user.add_roles(muted_role)
                await self.log(ctx, f"Temp muted {user.name} for warning accumulation")
                await user.send(f"Muteado en **{ctx.guild.name}** durante 12h por acumulación de avisos")
            else:
                muted_role = await ctx.guild.create_role(name="Muted role", permissions=discord.Permissions.none(), colour=discord.Color.dark_grey(), hoist=True)
                for channel in ctx.guild.channels:
                    await channel.set_permissions(muted_role, reason="Muted role",send_messages=False)
                for cnt in range(6):
                    try:
                        muted_role = discord.utils.get(ctx.guild.roles, name="Muted role")
                        await muted_role.edit(position=(len(ctx.guild.roles)-cnt))
                        print(1)
                    except:
                        pass
                await user.add_roles(muted_role)
                await user.send(f"Has sido muteado en **{ctx.guild.name}** durante 12h por acumulación de avisos")
            await asyncio.sleep(43200)
            await user.remove_roles(muted_role)
        elif warns[str(user.id)] == 10:
            await user.send(f"Has sido expulsado de **{ctx.guild.name}** por acumulación de avisos")
            await user.kick(reason="Too many warns")
            msg = await ctx.send(f'{user.id} kicked!')
            await self.log(ctx, f'{user.id} was kicked by {ctx.message.author}')
            await msg.delete(delay=2)
        elif warns[str(user.id)] == 15:
            await user.send(f"Has sido baneado de **{ctx.guild.name}** por acumulación excesiva de avisos. No molestes en otros servidores! GLHF!!")
            await user.ban(reason=reason)
            msg = await ctx.send(f'{user.id} banned!')
            await self.log(ctx, f'{user.id} was banned by {ctx.message.author}')
            await msg.delete(delay=2)

def setup(client):
    client.add_cog(Mod(client))
