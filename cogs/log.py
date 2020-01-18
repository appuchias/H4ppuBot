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
    print(f"Log: {msg}")

    with open("logs/modlog.txt", "a") as f:
        f.write(f"Log: {msg}\n")
