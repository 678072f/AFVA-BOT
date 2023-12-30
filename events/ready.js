const { Events } = require('discord.js');

const timeStamp = new Date(Date.now()).toISOString();

module.exports = {
    name: Events.ClientReady,
    once: true,
    execute(client) {
        console.log(`${timeStamp} [INFO] AFVA-BOT v2.0.0 development version ready!\n${timeStamp} [INFO] Logged into ${client.guilds.cache.map(r => `${r.name}`)} as ${client.user.tag}`);
    },
};