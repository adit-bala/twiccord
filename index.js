require('dotenv').config()
const { Client, GatewayIntentBits, Partials } = require('discord.js');

const client = new Client({ intents: [GatewayIntentBits.Guilds], partials: [Partials.Channel] });

client.once("ready", (c) => {
  console.log(`Ready! Logged in as ${c.user.tag}`);
});

client.login(process.env.DISCORD_TOKEN);
