require("dotenv").config();
const { Client, Intents, MessageEmbed } = require("discord.js");
const client = new Client({ intents: [Intents.FLAGS.GUILDS] });

client.once("ready", (c) => {
  console.log(`Ready! Logged in as ${c.user.tag}`);
  const channel = client.channels.cache.get("998417693608792124");
  channel.send({ content: "Hello!" });
  const twitterEmbed = new MessageEmbed()
	.setColor('#0099ff')
	.setTitle('Yo!')
	.setURL('https://twitter.com/existentialraj')
	.setAuthor({ name: 'Adit', iconURL: 'https://i.imgur.com/qlbr1Q0.jpg', url: 'https://discord.js.org' })
	.setDescription('Some description here')
	.setThumbnail('https://i.imgur.com/qlbr1Q0.jpg')
	.addFields(
		{ name: 'Regular field title', value: 'Some value here' },
		{ name: '\u200B', value: '\u200B' },
		{ name: 'Inline field title', value: 'Some value here', inline: true },
		{ name: 'Inline field title', value: 'Some value here', inline: true },
	)
	.addField('Inline field title', 'Some value here', true)
	.setImage('https://i.imgur.com/qlbr1Q0.jpg')
	.setTimestamp()
	.setFooter({ text: 'Bot created by Adit', iconURL: 'https://i.imgur.com/qlbr1Q0.jpg' });

channel.send({ embeds: [twitterEmbed] });
});



client.login(process.env.DISCORD_TOKEN);
