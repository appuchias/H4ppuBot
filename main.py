import discord
from discord.ext import commands, tasks

import os, pytz, log, random
from datetime import datetime as dt  # dt.now(tz).strftime("%H:%M:%S %d/%m/%Y")
from keep_alive import keep_alive

prefix = "*"
version = "1.1"
tz = pytz.timezone("Europe/Madrid")

client = commands.Bot(command_prefix=prefix)
client.remove_command("help")


@client.event
async def on_ready():
    print("Connected as:")
    print("{}: {}".format(client.user.name, client.user.id))
    print(f"Prefix: {prefix}")
    print(dt.now(tz).strftime("%H:%M:%S %d/%m/%Y"))
    print("--------------")
    change_status.start()
    game = discord.Game(name=f"*help | {client.user.name} | By Appu")
    await client.change_presence(activity=game)


# Emergency load
@client.command(hidden=True)
@commands.check(commands.is_owner())
async def emload(ctx, extension):
    client.load_extension(f"cogs.COG_{extension}")
    await ctx.send(f"Carga de emergencia de la extensión {extension}")


keep_alive()

# Alterned current statuses
activities = [
    f"*help | Bot Oficial | V{version}",
    f"*help | H4ppu Bot | By Appu",
    f"*help | Bot Oficial | V{version}",
    f"*help | H4ppu Bot | By Appu",
    f"*help | Bot Oficial | V{version}",
    f"*help | H4ppu Bot | By Appu",
    f"*help | Bot Oficial | V{version}",
    f"*help | H4ppu Bot | By Appu",
    "Verdad que mola?",
    "Nunca lo creerías",
    "Estaré donde no me esperas",
    "Hago ¡CHAS! y aparezco a tu lado",
    "Guarda una golosina para mí",
    "F",
    "No juzgues a un pez por su habilidad de trepar árboles...",
    "/summon H4ppuBot",
    "#TeamCreepers",
    "Fan de Eustaquio",
    "Nadie me conoce xD",
    "Pirateo cuentas :)",
]


@client.command(hidden=True)
@commands.check(commands.is_owner())
async def logout(ctx):
    msg = await ctx.send("Desconectando...")
    await msg.delete(delay=2)
    await client.logout()


# Load all extensions
extensions = []
for filename in os.listdir("./cogs"):
    if str(filename).endswith(".py"):
        if "COG" in str(filename[:-3]):
            client.load_extension(f"cogs.{filename[:-3]}")
            extensions.append(filename[:-3])
print(f"{extensions} loaded!")

# Status
@tasks.loop(seconds=3)
async def change_status():
    await client.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching, name=random.choice(activities)
        )
    )


client.run(os.environ.get("Token_Bot"))
# os.environ.get("Token_Bot")
