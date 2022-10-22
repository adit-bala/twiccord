import os
import tweepy
import discord
from discord.ext import commands
import random
from dotenv import load_dotenv
load_dotenv()


intents = discord.Intents.default()
intents.members = True
intents.message_content = True

client = tweepy.Client(
    consumer_key=os.getenv('CONSUMER_KEY'),
    consumer_secret=os.getenv('CONSUMER_SECRET'),
    access_token=os.getenv('TWITTER_ACCESS_TOKEN'),
    access_token_secret=os.getenv('TWITTER_SECRET_TOKEN')
)



bot = commands.Bot(command_prefix='?', intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


@bot.command()
async def tweets(ctx):
    my_tweets = client.get_users_tweets(id=os.getenv('USER_ID'), user_auth=True, tweet_fields="created_at")
    embed=discord.Embed(title="Recent Tweets", description="Recent Tweets from @existentialraj", color=0xe8d1e7)
    embed.set_author(name=ctx.author.display_name, url="https://twitter.com/existentialraj", icon_url="https://i.imgur.com/riyrHKH.jpg")
    for tweet in my_tweets.data:
        embed.add_field(name=tweet.created_at, value=tweet.text)
        
    await ctx.send(embed=embed)


bot.run(os.getenv('DISCORD_BOT'))

