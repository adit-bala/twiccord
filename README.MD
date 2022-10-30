# twiccord

a discord bot that sends my friends tweets because they're too lazy to download twitter

## How To Set Up The Bot

### Requirements
- [Twitter Project](https://developer.twitter.com/en/portal/projects) set up
- [Discord Bot](https://discord.com/developers/applications) set up

### Installation

```
# Clone the repository
git clone https://github.com/TannerGabriel/discord-bot.git

# Enter into the directory
cd discord-bot/

# Install the dependencies
pip install -r requirements.txt

# Create .env file
touch .env
```

### Setting up environment variables
There are number of environment variables you need to add in `.env` before running the app
```
CONSUMER_KEY='INSERT_TWITTER_API_KEY'
CONSUMER_SECRET='INSERT_TWITTER_API_SECRET'
TWITTER_ACCESS_TOKEN='INSERT_TWITTER_ACCESS_TOKEN'
TWITTER_SECRET_TOKEN='INSERT_TWITTER_SECRET_TOKEN'
DISCORD_BOT='INSERT_DISCORD_TOKEN_HERE'
USER_ID="INSERT_TWITTER_USER_ID"
TWITTER_LINK="INSERT_TWITTER_LINK"
FRIEND_ID="INSERT_DISCORD_FRIEND_ID_THAT_YOU_WANT_TO_BOTHER"
```

### Required permissions

Make sure that your bot has the `applications.commands` application scope enabled, which can be found under the `OAuth2` tab on the [developer portal](https://discord.com/developers/applications/)

Enable the `Server Members Intent` and `Message Content Intent` which can be found under the `Bot` tab on the [developer portal](https://discord.com/developers/applications/)

## Starting the bot
```
python3 bot.py
```

## Deploying the bot

[Add Google Cloud Instructions]
