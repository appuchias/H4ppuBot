import discord
from discord.ext import commands, tasks
from igramscraper.instagram import Instagram
from twitter_scraper import get_tweets

class InstaCog(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.ig = Instagram()

    @commands.command()
    async def insta(self, ctx, perfil: str = None):
        try:
            all_medias = self.ig.get_medias(perfil, 10)
        except Exception as error:
            await ctx.send("Error: ", error)
            return
        for img in all_medias:
            if img.type == "image":
                embed = discord.Embed(title=f"Última imagen de [{perfil}] en Instagram", description="By Mr. Appu™", url=img.image_high_resolution_url, color=0xf03c4d)
                embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                embed.set_image(url=img.image_high_resolution_url)
                embed.add_field(name="Pie de foto:", value=img.caption, inline=True)
                embed.add_field(name="Likes:", value=img.likes_count, inline=True)
                embed.add_field(name="Comentarios:", value=img.comments_count, inline=True)
                await ctx.send(embed=embed)
                return

    @commands.command()
    async def twitter(self, ctx, user: str = None):
        if user == None:
            await ctx.send("Especifica usuario que buscar")

        embed = discord.Embed(title=f"Últimos 10 tweets de {user}", description="By Mr. Appu™", color=0x1da1f3, url=f"https://twitter.com/{user}")

        cnt = 1
        for tweet in get_tweets(user, pages=1):
            embed.add_field(name=f"**Tweet** ***{cnt}*** **de 10**", value=f"```{(tweet['text']).replace('pic', 'https://pic')}```:heart: {tweet['likes']}      -      :repeat: {tweet['retweets']}\n(https://twitter.com/{user}/status/{tweet['tweetId']})", inline=False)
            if cnt >= 10:
                await ctx.send(embed=embed)
                return
            cnt += 1

def setup(client):
    client.add_cog(InstaCog(client))
