const { SlashCommandBuilder } = require('discord.js');

module.exports = {
    cooldown: 5,
	data: new SlashCommandBuilder()
		.setName('log')
		.setDescription('Download log file'),
	async execute(interaction) {
		await interaction.send({ files: '../log.txt' });
	},
};