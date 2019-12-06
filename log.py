import discord
from datetime import datetime as dt
import pytz

tz = pytz.timezone("Europe/Madrid")
local = dt.now(tz)

async def log(ctx, msg):
    channel = discord.utils.get(ctx.guild.text_channels, name="log")
    if channel in ctx.guild.text_channels:
        pass
    else:
        await ctx.send("Error 404. Channel not found")
        return

    await channel.send(msg)
    print(f"({local.strftime("%H:%M:%S %d/%m/%Y")})Log: {msg}")

    with open("modlog.txt", "a") as f:
        f.write(f"({local.strftime("%H:%M:%S %d/%m/%Y")})Log: {msg}\n")
