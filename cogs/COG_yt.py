import discord
from discord.ext import commands, tasks
import asyncio, typing

import urllib.request
from bs4 import BeautifulSoup

class Yt(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def yt(self, ctx, internal: typing.Optional[bool]= False, *, busqueda):
        results = []
        embed = discord.Embed(title=f"5 primeros resultados de {busqueda} en YouTube", description="By Mr. Appu™", color=discord.Colour.red())
        query = urllib.parse.quote(busqueda)
        url = "https://www.youtube.com/results?search_query=" + query
        response = urllib.request.urlopen(url)
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')

        for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}, limit=5+1):
            url = 'https://www.youtube.com' + vid['href']
            if not "user" in url:
                results.append(url)
                embed.add_field(name=vid["title"], value=url, inline=False)

        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Yt(client))
