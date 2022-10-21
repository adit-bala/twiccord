import os
import tweepy
from dotenv import load_dotenv
load_dotenv()

client = tweepy.Client(
    consumer_key=os.getenv('CONSUMER_KEY'),
    consumer_secret=os.getenv('CONSUMER_SECRET'),
    access_token=os.getenv('TWITTER_ACCESS_TOKEN'),
    access_token_secret=os.getenv('TWITTER_SECRET_TOKEN')
)

my_tweets = client.get_users_tweets(id="1544355617627709440", user_auth=True)



# res = client.get_home_timeline()

if not os.path.isfile('./output.txt'):
    f = open('./output.txt', 'x')
with open('output.txt', 'w') as f:
    # for line in my_tweets:
    #     f.write(str(line))
    f.write(str(my_tweets))



