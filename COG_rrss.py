import discord
from discord.ext import commands, tasks
from igramscraper.instagram import Instagram
from twitter_scraper import get_tweets
import praw

version = "0.4"
reddit = praw.Reddit(client_id='08Zc5gTPSZ_fzg', client_secret="6xvK-ER8x59HLJyHtKjyRU653yA", user_agent=f"H4ppu bot V. {version}")

class RrSs(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.ig = Instagram()

    @commands.command()
    async def insta(self, ctx, perfil: str = None):
        all_medias = self.ig.get_medias(perfil, 10)
        try:
            x = all_medias[0]
        except IndexError:
            await ctx.send("La cuenta es privada! :confused:")
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

    @commands.command(name="reddit")
    async def _reddit(self, ctx, query: str = "all"):
        subreddit = reddit.subreddit(query)
        if subreddit.over18 and not ctx.channel.is_nsfw():
            await ctx.send("Contenido NSFW\nPrueba en un canal con NSFW activado!")
            return
        embed = discord.Embed(title=f"Últimos 10 posts del subreddit {query}", description="By Mr. Appu™", color=0xff4500, url=f"https://www.reddit.com/r/{subreddit.display_name}")
        cnt = 1
        for submission in subreddit.hot(limit=10):
            embed.add_field(name=f"**Post** ***{cnt}*** **de 10**", value=f"{submission.title}\nLink: https://reddit.com{submission.permalink}", inline=False)
            if cnt >= 10:
                await ctx.send(embed=embed)
                return
            cnt += 1

def setup(client):
    client.add_cog(RrSs(client))
