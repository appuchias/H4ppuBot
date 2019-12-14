import discord
from discord.ext import commands, tasks
from igramscraper.instagram import Instagram
from twitter_scraper import get_tweets

class InstaCog(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.ig = Instagram()

    @commands.command()
    async def insta(self, ctx, user: str = None):
        if user == None:
            await ctx.send("Especifica usuario que buscar")
        try:
            all_medias = self.ig.get_medias(user, 10)
        except Exception as error:
            await ctx.send("Error: ", error)
            return
        last_pic = all_medias[0]
        if last_pic.type == "image":
            embed = discord.Embed(title=f"Última imagen de [{user}] en Instagram", description="By Mr. Appu™", url=last_pic.image_high_resolution_url, color=0xf03c4d)
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            embed.set_image(url=last_pic.image_high_resolution_url)
            embed.add_field(name="Pie de foto:", value=last_pic.caption, inline=True)
            embed.add_field(name="Likes:", value=last_pic.likes_count, inline=True)
            embed.add_field(name="Comentarios:", value=last_pic.comments_count, inline=True)
            await ctx.send(embed=embed)

    @commands.command()
    async def twitter(self, ctx, user: str = None):
        if user == None:
            await ctx.send("Especifica usuario que buscar")
        embed = discord.Embed(title="Twitter info", description="By Appu")
        for tweet in get_tweets(user, pages=1):
            embed.add_field(name=f"Tweet", value=f"{(tweet['text']).replace('pic', 'https://pic')}\n{tweet['likes']} likes <3!\nTweet: https://twitter.com/{user}/status/{tweet['tweetId']}", inline=False)
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(InstaCog(client))
