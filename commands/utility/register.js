const { SlashCommandBuilder } = require('discord.js');
const { regUrl } = require('../../config.json');

module.exports = {
    cooldown: 5,
	data: new SlashCommandBuilder()
		.setName('register')
		.setDescription('Use this command to connect your Discord account to your AFVA profile.'),
	async execute(interaction) {
		await interaction.reply({ content: `Use this link to register your Discord to your AFVA Profile: ${regUrl}${interaction.user.id}`, ephemeral: true });
	},
};