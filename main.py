import discord
from discord.ext import commands, tasks
import os
from itertools import cycle
from keep_alive import keep_alive

prefix = "*"
version = "0.2.3 development"

client = commands.Bot(command_prefix=prefix)
client.remove_command('help')

@client.event
async def on_ready():
    print('Connected as:')
    print('{}: {}'.format(client.user.name, client.user.id))
    print('Prefix: *')
    print('--------------')
    change_status.start()
    game=discord.Game(name=f"*help | {client.user.name} | By Appu")
    await client.change_presence(activity=game)

#Emergency load
@client.command(hidden=True)
@commands.check(commands.is_owner())
async def emload(ctx, extension):
    client.load_extension(f'Cogs.{extension}')
    await ctx.send(f'Extensión {extension} cargada!')

@client.command()
async def help(ctx):
    embed=discord.Embed(title='Help Command', description="H4ppu Bot", color=0x7289DA)
    embed.set_thumbnail(url=client.user.avatar_url)
    embed.set_footer(text=f'(By: {ctx.author}) | | <> - Requerido, [] - Opcional | | Todos los comandos se añaden a log', icon_url=ctx.author.avatar_url)

    embed.add_field(name='`~General~`', value='**Comandos generales**', inline=False)
    embed.add_field(name='*help', value='Muestra este comando', inline=False)
    embed.add_field(name='*prefix <prefijo>', value="Cambia el prefijo del bot [Solo Propietario]", inline=False)
    embed.add_field(name='`~Mod~`', value='**Comandos de moderación** [Solo Mods]', inline=False)
    embed.add_field(name='*clear <n>', value='Elimina hasta 20 mensajes', inline=False)
    embed.add_field(name='*kick <@member> [motivo]', value='Echa a alguien', inline=False)
    embed.add_field(name='*ban <@member> [motivo]', value='Banea a alguien', inline=False)
    embed.add_field(name='*unban <nombre del miembro>', value='Elimina el ban al miembro especificado', inline=False)
    embed.add_field(name='*warn <@member> [motivo]', value="Avisa a alguien. Especifica motivo por favor", inline=False)
    embed.add_field(name='*mute <@member>', value="Mutea a alguien", inline=False)
    embed.add_field(name='*tmute <@member> <tiempo(minutos)>', value="Mutea a alguien durante el tiempo que le digas", inline=False)
    embed.add_field(name='`~Basic~`', value='**Comandos básicos**', inline=False)
    embed.add_field(name="*load <Extensión>", value="Carga la extensión que le digas [Only Mods]", inline=False)
    embed.add_field(name="*unload <Extensión>", value="Descarga la extensión que le digas [Only Mods]", inline=False)
    embed.add_field(name="*reload <Extensión>", value="Recarga la extensión que le digas [Only Mods]", inline=False)
    embed.add_field(name='`~Chat~`', value='**Comandos con respuestas en el chat directas**', inline=False)
    embed.add_field(name='*ping', value='Responde Pong! Usado para medir la latencia', inline=False)
    embed.add_field(name='*di <msg>', value='Dice lo que pongas.', inline=False)
    embed.add_field(name='*reverse <msg>', value='Dice al revés lo que pone.', inline=False)
    embed.add_field(name='*repite <veces> <msg>', value='Repite lo que quieras hasta 10 veces.', inline=False)
    embed.add_field(name='*suma <n1> <n2> <n3>', value='Suma hasta 3 números.', inline=False)
    embed.add_field(name='*dado <n de caras>', value='Tira un dado de cualquier número de caras.', inline=False)
    embed.add_field(name='*moneda', value='Lanza una moneda.', inline=False)
    #embed.add_field(name=f'*', value=None, inline=False)
    await ctx.send(embed=embed)

#Blinking current statuses
activities = cycle([f"*help | Aún en desarrollo... | V{version}", f"*help | H4ppu Bot"])

@client.command(hidden=True)
@commands.check(commands.is_owner())
async def logout(ctx):
    msg = await ctx.send('Desconectando...')
    await msg.delete(delay=2)
    await client.logout()

#Load all extensions
extensions=[]
for filename in os.listdir('./Cogs'):
    if str(filename).endswith('.py'):
        client.load_extension(f'Cogs.{filename[:-3]}')
        extensions.append(filename[:-3])
print(f'{extensions} loaded!')


#Tasks
keep_alive()

#Status
@tasks.loop(seconds=3)
async def change_status():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=next(activities)))

client.run(os.environ.get("Token_Bot"))
#os.environ.get("Token_Bot")
