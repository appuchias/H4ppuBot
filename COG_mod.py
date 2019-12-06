import asyncio
import json
import discord
from discord.ext import commands
import log

class Mod(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.client.log = self.log

    #When a message is sent
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or message.channel.id == 637356734649729044:
            return
        user = message.author
        bad_words = ["puta", "puto", "gilipollas", "hijo de", "cabron", "cabrón", "pvta", "pvto", "pta", "pto", "p*to", "p*ta", "asshole"]
        for word in bad_words:
            if word in message.content.lower():
                await self.warning(user, user, f"Used a bad word ({word})")
                await log.log(user, f"{user} used a bad word ({word})")
        if "cucaracha" in message.content.lower():
            if message.author.id == 395672084451295242:
                for cnt in range(0, 5):
                    await message.author.send("Nadie quiere oír eso...\n\t\t\t\t\t\t~Appu")
                    await asyncio.sleep(1)
                    cnt += 1

    #Commands
    #Bulk message delete
    @commands.command()
    @commands.has_role("Mods")
    async def clear(self, ctx, number):
        n = number
        if int(n) > 20:
            await ctx.send('Demasiados mensajes para eliminar...')
            return
        await ctx.channel.purge(limit=(int(n)+1))
        msg = await ctx.send(f'{str(n)} mensaje(s) eliminados!')
        print(f'{str(n)} messages cleared in #{ctx.channel.name}')
        await log.log(ctx, f'{str(n)} messages cleared in #{ctx.channel.name} by {ctx.message.author}')
        await msg.delete(delay=2)

    #Kick someone
    @commands.command()
    @commands.has_role("Mods")
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f'{member} kickeado!')
        await log.log(ctx, f'{member} was kicked by {ctx.message.author}')
        await ctx.message.delete(delay=2)

    #Ban someone
    @commands.command()
    @commands.has_role("Mods")
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f'{member} baneado!')
        await log.log(ctx, f'{member} was banned by {ctx.message.author}')
        await ctx.message.delete(delay=2)

    # #Unban someone
    # @commands.command()
    # @commands.has_role("Mods")
    # async def unban(self, ctx, *, member):
    #     banned_users = await ctx.guild.bans()
    #     name, discr = member.split('#')

    #     for ban_entry in banned_users:
    #         user = ban_entry.user
    #         if(user.name, user.discriminator) == (name, discr):
    #             await ctx.guild.unban(user)
    #             await log.log(ctx, f'{user} was unbanned by {ctx.message.author}')
    #     await ctx.send(f'{member} desbaneado!')
    #     await ctx.message.delete(delay=2)

    @commands.command()
    @commands.has_role("Mods")
    async def warn(self, ctx, user:discord.Member, *, reason = "None"):
        await self.warning(ctx, user, reason)
        await log.log(ctx, f"{ctx.author} warned {user.name}!")
        await ctx.send(f"{user.name} fue alertado por {ctx.author}")
        await ctx.message.delete(delay=2)


    @commands.command()
    @commands.has_role("Mods")
    async def mute(self, ctx, user: discord.Member):
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted role")
        await user.add_roles(muted_role)
        await log.log(ctx, f"{user.name} got muted!")

    @commands.command()
    @commands.has_role("Mods")
    async def tmute(self, ctx, user: discord.Member, n:int):
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted role")
        await user.add_roles(muted_role)
        await log.log(ctx, f"{user.name} got muted for {n}m!")
        await asyncio.sleep(n*60)
        await user.remove_roles(muted_role)

    @commands.command()
    @commands.has_role("Mods")
    async def report(self, ctx, who : discord.Member, *, reason = "no reason"):
        author = ctx.author
        channel = discord.utils.get(ctx.guild.channels, name="reports")
        appu = discord.utils.get(ctx.guild.members, id=455321214525767680)

        with open("reports.json") as r:
            reports = json.loads(r.read())

        if not str(who.id) in reports:
            reports[str(who.id)] = 0
        reports[str(who.id)] += 1

        case = 0
        for n in reports:
            case += reports[n]
        await appu.send(f"{author.mention} reported {who.mention} for **[{reason}]** and now has **[{reports[str(who.id)]}]** reports!")
        await channel.send(f"▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄\nCase **{case}**:\n - Member: **{who}**\n - Actual reports: **{reports.get(str(who.id))}**\n - Reason: *{reason}*")

        if reports.get(str(who.id)) >= 3:
            await appu.send(f"[{who}] has [{reports.get(str(who.id))}] reports! Be aware!")

        with open("reports.json", "w") as w:
            w.write(json.dumps(reports, indent=4))

        await log.log(ctx, f"{ctx.author} reported {who.mention} for {reason}")
        await ctx.message.delete(delay=2)

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

    #Warn function
    async def warning(self, ctx, user, reason):
        with open("warns.json", "r") as f:
            warns = json.load(f)

        if not str(user.id) in warns:
            warns[str(user.id)] = 0
        warns[str(user.id)] += 1

        await user.send(f"Fuiste avisado por: {reason}\nTienes {warns[str(user.id)]} avisos. **Ten cuidado!**:warning:\n||Con 3 avisos: Muteo de 1h.\tCon 5 avisos: Muteo de 12h.\tCon 10 avisos: Expulsión.\tCon 15 avisos: Baneo permanente no revisable.\n*Los avisos se guardan aunque te vayas y vuelvas a entrar!*||")
        with open("warns.json", "w") as f:
            json.dump(warns, f, indent=4)

        if warns[str(user.id)] == 3:
            muted_role = discord.utils.get(ctx.guild.roles, name="Muted role")
            try:
                for channel in ctx.guild.channels:
                    await channel.set_permissions(muted_role, reason="Muted role",send_messages=False)
                await user.add_roles(muted_role)
                await log.log(ctx, f"Temp muted {user.name} for warning accumulation")
                await user.send(f"You got muted in **{ctx.guild.name}** for 1h for warning accumulation")
            except:
                print("Warn exception in 1h mute")
            await asyncio.sleep(3600)
            await user.remove_roles(muted_role)

        elif warns[str(user.id)] == 5:
            muted_role = discord.utils.get(ctx.guild.roles, name="Muted role")
            if muted_role in ctx.guild.roles:
                for channel in ctx.guild.channels:
                    await channel.set_permissions(muted_role, reason="Muted role",send_messages=False)
                await user.add_roles(muted_role)
                await log.log(ctx, f"Temp muted {user.name} for warning accumulation")
                await user.send(f"Muteado en **{ctx.guild.name}** durante 12h por acumulación de avisos")
            await asyncio.sleep(43200)
            await user.remove_roles(muted_role)

        elif warns[str(user.id)] == 10:
            await user.send(f"Has sido expulsado de **{ctx.guild.name}** por acumulación de avisos")
            await user.kick(reason="Too many warns")
            await ctx.send(f'{user.id} kickeado!')
            await log.log(ctx, f'{user.id} was kicked by {ctx.message.author}')

        elif warns[str(user.id)] == 15:
            await user.send(f"Has sido baneado de **{ctx.guild.name}** por acumulación excesiva de avisos. No molestes en otros servidores! GLHF!!")
            await user.ban(reason=reason)
            await ctx.send(f'{user.id} baneado!')
            await log.log(ctx, f'{user.id} was banned by {ctx.message.author}')

def setup(client):
    client.add_cog(Mod(client))
