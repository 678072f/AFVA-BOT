const { SlashCommandBuilder } = require('discord.js');
const { syncUrl } = require('../../config.json');

module.exports = {
    cooldown: 5,
	data: new SlashCommandBuilder()
		.setName('sync')
		.setDescription('Use this command to connect your Discord account to your AFVA profile.'),
	async execute(interaction) {
		const userData = await fetch(`${syncUrl}${interaction.user.id}`).then((res) => res.json());
        let nickName = userData.firstName + ' ' + userData.lastName + ' | ' + userData.pilotCode;
        if (!userData.pilotCode) {
            nickName = userData.firstName + ' ' + userData.lastName + '|NEW PILOT';
        }

        if (nickName.length > 32) {
            return;
        }

        interaction.member.setNickname(nickName);
	},
};