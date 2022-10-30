import os
import tweepy
import discord
import calendar
import asyncio
from discord.ext import commands, tasks
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

# get <arg> tweets
@bot.command()
async def num(ctx, arg=5):
    # ensure that range falls within the past 100 tweets, else default to 50
    tweets_range = arg if 0 < arg < 100 else 50
    # fetch tweets
    my_tweets = client.get_users_tweets(id=os.getenv(
        'USER_ID'), user_auth=True, tweet_fields=["referenced_tweets", "conversation_id", "created_at"], max_results=100, exclude="retweets")
    # calculate the range between today and the last tweet fetched
    delta = datetime.today().date() - my_tweets.data[tweets_range-1].created_at.date()
    # init discord embed and link to twitter
    embed = discord.Embed(
        title=f"ruminations from the past {delta.days} days", color=0xe8d1e7)
    # show the user who requested tweets as the author
    embed.set_author(name=ctx.author.display_name, url=os.getenv(
        'TWITTER_LINK'),
                     icon_url=ctx.author.avatar)
    # create set to keep track to avoid tweets that are present in a thread
    seen_tweets = set()
    # iterate through tweets
    for i in range(tweets_range):
        tweet = my_tweets.data[i]
        # check if tweet displayed in previous thread
        if tweet.id in seen_tweets:
            continue
        # check if tweet is a reply to another tweet
        if tweet.referenced_tweets:
            # attach entire conversation from tweet
            attach_conversation(embed, tweet, seen_tweets, month=True)
            continue
        attach_month(embed, tweet)
    # roast my friends for making me create this bot (jk, I made this for my friends)
    embed.set_footer(
        text=f"{ctx.author.display_name} is too lazy to download twitter")
    await ctx.send(embed=embed)

# get tweets from today
@bot.command()
async def today(ctx):
    await fetch_today_tweets(ctx)

async def fetch_today_tweets(ctx, periodic=False):
    # get tweets from today and convert them to twitter's sus format
    today = datetime.today().isoformat()[:-7] + "Z"
    # fetch tweets
    my_tweets = client.get_users_tweets(id=os.getenv(
        'USER_ID'), user_auth=True, tweet_fields="created_at", exclude="retweets", start_time=today)
    
    # print message if there are no tweets from today
    if not my_tweets.data:
        await ctx.send(f"No tweets yet today :(")
        return
    embed = discord.Embed(
        title="today's thoughts", color=0xe8d1e7)
    # keep track of threaded tweets
    seen_tweets = set()
    # iterate through tweets
    for tweet in my_tweets.data:
        if tweet.id in seen_tweets:
            continue
        # check if tweet is a reply to another tweet
        if tweet.referenced_tweets:
            # attach entire conversation from tweet
            attach_conversation(embed, tweet, seen_tweets, month=False)
            continue
        # obtain time from tweet in PST timezone
        attach_today(embed, tweet)
    if periodic:
        embed.set_footer(text="?help")
        await ctx.send(f"Here you go mf {os.getenv('FRIEND_ID')}")
    await ctx.send(embed=embed)

def attach_month(embed, tweet, inline=False):
    # obtain date from tweet
    date = tweet.created_at.replace(
        tzinfo=timezone.utc).astimezone(tz=None).date()
    # obtain time from tweet in PST timezone
    time = tweet.created_at.replace(
        tzinfo=timezone.utc).astimezone(tz=None).time()
    # format date and time within embed
    embed.add_field(
        name=f"{calendar.month_name[date.month]} {date.day}, {date.year} at {datetime.strptime(str(time)[:-3],'%H:%M').strftime('%I:%M %p')}", value=tweet.text, inline=inline)

def attach_today(embed, tweet, inline=False):
    # obtain time from tweet in PST timezone
    time = tweet.created_at.replace(
        tzinfo=timezone.utc).astimezone(tz=None).time()
    embed.add_field(
        name=f"@ {datetime.strptime(str(time)[:-3],'%H:%M').strftime('%I:%M %p')}", value=tweet.text, inline=inline)

def attach_conversation(embed, tweet, seen_tweets, month):
    attatch_format = attach_month if month else attach_today
    # list of tweets in thread
    conversation = []
    # lookup current tweet
    curr = client.get_tweet(id=tweet.id, user_auth=True, tweet_fields=["referenced_tweets", "created_at"], expansions=["referenced_tweets.id"])
    # iterate through replies until reaching the root tweet (pseudo-linked list behavior)
    while curr:
        # keep track of seen tweets
        seen_tweets.add(curr.data.id)
        # add tweet to thread list
        conversation.append(curr)
        # break if at root tweet
        if not curr.includes:
            break
        # find tweet replied to
        curr = client.get_tweet(id=curr.includes['tweets'][0].id, user_auth=True, tweet_fields=["referenced_tweets", "created_at"], expansions=["referenced_tweets.id"])
    # iterate through tweets starting from root
    for tweet in conversation[::-1]:
        attatch_format(embed, tweet.data, inline=True)

@tasks.loop(hours=24)
async def my_task():
    await bot.wait_until_ready()
    channel = bot.get_channel(1000514894334017607)
    await fetch_today_tweets(channel, periodic=True)


async def main():
    async with bot:
        my_task.start()
        await bot.start(os.getenv('DISCORD_BOT'))

asyncio.run(main())
