/* eslint-disable no-shadow */
const { SlashCommandBuilder } = require('discord.js');
const { syncUrl } = require('../../config.json');
const { DISCORD_ROLES_MAP } = require('../../constants-dev');

module.exports = {
    cooldown: 5,
	data: new SlashCommandBuilder()
		.setName('sync')
		.setDescription('Use this command to sync your Discord roles with your AFVA profile.')
        .addUserOption(option =>
            option.setName('target')
                .setDescription('Member to sync')
                .setRequired(false)),
	async execute(interaction) {
        const target = interaction.options.getUser('target');
        let nickName;
        let userData;

        if (target) {
            userData = await fetch(`${syncUrl}${target.id}`).then((res) => res.json());
            nickName = userData.firstName + ' ' + userData.lastName + ' | ' + userData.pilotCode;
        }
        else {
            userData = await fetch(`${syncUrl}${interaction.user.id}`).then((res) => res.json());
            nickName = userData.firstName + ' ' + userData.lastName + ' | ' + userData.pilotCode;
        }

        if (!userData.pilotCode) {
            nickName = userData.firstName + ' ' + userData.lastName + '|NEW PILOT';
        }

        if (nickName.length > 32) {
            return;
        }
        try {
            interaction.member.setNickname(nickName);
        }
        catch (err) {
            console.log(`There was a problem changing ${interaction.user.nickName}'s nickname: `, err);
        }
            await interaction.reply({ content: `${interaction.user}'s roles are: ${userData.roles}\n Nickname: ${nickName}` });

        try {
            userData.roles.forEach((roleName) => {
                const guild = interaction.guild;
                const role = guild.roles.cache.find(role => role.id === DISCORD_ROLES_MAP[roleName]);
                const member = interaction.member;
                try {
                    if (role) {
                        member.roles.add(role);
                    }
                    console.log(role);
                }
                catch (err) {
                    console.log(err);
                }
            });
        }
        catch (err) {
            console.log(err);
        }
	},
};