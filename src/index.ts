import "dotenv/config";

import { Client, IntentsBitField } from "discord.js";

const client = new Client({
	intents: Object.values(IntentsBitField.Flags).filter(
		(x): x is number => typeof x === "number"
	),
	allowedMentions: {
		repliedUser: false
	}
});

client.on("ready", client => {
	console.log(`Logged in as ${client.user.tag}!`);
});

client.on("messageCreate", message => {
	if (message.content === "ping") {
		message.reply("pong");
	}
});

client.login(process.env.DISCORD_TOKEN);
