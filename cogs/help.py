import discord
import asyncio
from discord.ext import commands
from discord.errors import Forbidden

# Function to send embedded message
async def sendEmbed(ctx, emb):
    try:
        await ctx.send(embed=emb)
    except Forbidden:
        try:
            await ctx.send("I don't have permission to embed. Please have @IT check bot permisssions.")
        except Forbidden:
            await ctx.author.send(
                f"Hey {ctx.author.mention}, I don't have permission to send messages in {ctx.channel.name} on {ctx.guild.name}\n"
                f"Please inform info@afva.net about this issue and we will resolve it as soon as possible! :slight_smile: ", embed=emb
            )


# Help Menu Class
class Help(commands.Cog):
    # Constructor
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def help(self, ctx, *input):
        # Setup COG functionality
        prefix = '$'
        version = "1.0"
        
        # Set owner name
        owner = '0995'
        owner_name = 'danielgduhon#0995'

        # Check if COG parameter was given
        if not input:
            try:
                owner = ctx.guild.get_member(owner).mention
            except AttributeError as e:
                owner = owner

            # Build Embed
            EMBED = discord.Embed(title='Commands and modules', color=discord.Color.blue(), description = f"Available commands and corrct usage. Use `{prefix}help <module>` to see more information about that module (NOTE that this does not work yet).\n")

            # Iterate through COGS
            cogs_desc = ''
            for cog in self.bot.cogs:
                cogs_desc += f'`{cog}` {self.bot.cogs[cog].__doc__}\n'

            # Add cogs to embed
            EMBED.add_field(name = 'Modules', value = cogs_desc, inline = False)

            # Iterating through uncategorized commands
            commands_desc = ''
            for command in self.bot.walk_commands():
                if not command.cog_name and not command.hidden:
                    commands_desc += f'```{command.name}: {command.help}```\n'
            
            # Add commands to embed
            if commands_desc:
                EMBED.add_field(name = 'Not belonging to a module', value = commands_desc, inline = False)

            # Set author info
            EMBED.add_field(name = "About", value = f"The AFVA-BOT is developed by {owner_name}, based on discord.py.\n\
                            Please email info@afva.net or dduhon@afva.net with any issues/suggestions.")
            EMBED.set_footer(text = f"Bot is running {version}")

        elif len(input) == 1:
            for cog in self.bot.cogs:
                if cog.lower() == input[0].lower():
                    # Make title, getting description
                    EMBED = discord.Embed(title = f'{cog} - Commands', description = self.bot.cogs[cog].__doc__, color = discord.Color.green())

                    for command in self.bot.get_cog(cog).get_commands():
                        if not command.hidden:
                            EMBED.add_filed(name = f"`{prefix}{command.name}`", value = command.help, inline = False)
                            # Found cog, break loop
                            break
        
                        else:
                            EMBED = discord.Embed(title = "Unknown Command!", description = f"The command `{input[0]}` is not known by AFVA-BOT.", color = discord.Color.orange())

        elif len(input) > 1:
            EMBED = discord.Embed(title = "Too many inputs:", description = "Please request only 1 module at a time.", color = discord.Color.orange())
        
        else:
            EMBED = discord.Embed(title = "What's happening out there?", description = "Shall I describe it to you?\n ... \nOr would you like me to find you a box?\n I don't know how you got here, but something went wrong. Please report to info@afva.net", color = discord.Color.red())

        await sendEmbed(ctx, EMBED)

async def setup(bot):
    await bot.add_cog(Help(bot))