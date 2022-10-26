import os
import tweepy
import discord
import calendar
from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime, timezone


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
async def num(ctx, arg=5):
    my_tweets = client.get_users_tweets(id=os.getenv(
        'USER_ID'), user_auth=True, tweet_fields="created_at", max_results=100, exclude="retweets")
    tweets_range = arg if 0 < arg < 100 else 50
    delta = datetime.today().date() - my_tweets.data[tweets_range-1].created_at.date()
    embed = discord.Embed(
        title=f"ruminations from the past {delta.days} days", color=0xe8d1e7)
    embed.set_author(name=ctx.author.display_name, url="https://twitter.com/existentialraj",
                     icon_url=ctx.author.avatar)
    for i in range(tweets_range):
        tweet = my_tweets.data[i]
        date = tweet.created_at.replace(
            tzinfo=timezone.utc).astimezone(tz=None).date()
        time = tweet.created_at.replace(
            tzinfo=timezone.utc).astimezone(tz=None).time()
        embed.add_field(
            name=f"{calendar.month_name[date.month]} {date.day}, {date.year} at {datetime.strptime(str(time)[:-3],'%H:%M').strftime('%I:%M %p')}", value=tweet.text, inline=False)
    embed.set_footer(
        text=f"{ctx.author.display_name} is too lazy to download twitter")
    await ctx.send(embed=embed)


@bot.command()
async def today(ctx):
    today = datetime.today().isoformat()[:-7] + "Z"
    my_tweets = client.get_users_tweets(id=os.getenv(
        'USER_ID'), user_auth=True, tweet_fields="created_at", exclude="retweets", start_time=today)
    if not my_tweets.data:
        await ctx.send("No tweets yet today :(")
        return
    embed = discord.Embed(
        title="today's thoughts", color=0xe8d1e7)
    for tweet in my_tweets.data:
        time = tweet.created_at.replace(
            tzinfo=timezone.utc).astimezone(tz=None).time()
        embed.add_field(
            name=f"@ {datetime.strptime(str(time)[:-3],'%H:%M').strftime('%I:%M %p')}", value=tweet.text, inline=False)
    await ctx.send(embed=embed)


bot.run(os.getenv('DISCORD_BOT'))
