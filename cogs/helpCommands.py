import discord, json
from discord.commands import slash_command
from discord.ext import commands


class helpCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Returns a list of commands available
    @slash_command(guild_ids=[925123755175460865, 709206749378248716, 960997598594994186], name="help", description="Sends the user a list of commands.")
    async def help(self, ctx):
        modRole = discord.utils.get(ctx.author.guild.roles, name="Moderator/character")
        if modRole in ctx.author.roles:
            myEmbed = discord.Embed(title="Mod Command List", description="<> = required field    [] = optional field", color=0x800080)
            myEmbed.add_field(name="Induct", value="Inducts a new user. Format: $induct <mention user>", inline=False)
            myEmbed.add_field(name="Printy", value="Prints all users information (use with caution). Format: $printy", inline=False)
            myEmbed.add_field(name="Get Data", value="Gets data for specified user. Format: $getData <mention user>", inline=False)
            myEmbed.add_field(name="Mod Bite", value="Lets the mods bite a user, no points are changed. Format: $modBite <user ID>", inline=False)
            myEmbed.add_field(name="unBite", value="Unbites a player and removes points. Format: $unbite <mention user>", inline=False)
            myEmbed.add_field(name="Cure", value="Cures a user. Format: $cure <mention user>", inline=False)
            myEmbed.add_field(name="Feast", value="Resets all zombie's starve timers. Format: $feast", inline=False)
            myEmbed.add_field(name="Add Upgrade", value="Adds an upgrade to a user. Format: $addUpgrade <mention user> <upgrade>", inline=False)
            myEmbed.add_field(name="Add Points", value="Adds points the the specified team. Format: $addPoints <Humans/Zombies> <number of points>", inline=False)
            myEmbed.add_field(name="Remove Points", value="Removes points the the specified team. Format: $removePoints <Humans/Zombies> <number of points>", inline=False)
            myEmbed.add_field(name="Add Player Points", value="Adds points the the specified player. Format: $addPlayerPoints <mention user> <number of points>",inline=False)
            myEmbed.add_field(name="Remove Player Points", value="Removes points the the specified player. Format: $removePlayerPoints <mention user> <number of points>", inline=False)
            myEmbed.add_field(name="Display Points", value="Displays the current points for both teams. Format: $displayPoints", inline=False)
            myEmbed.set_author(name="Shitbot")
            await ctx.author.send(embed=myEmbed)
            await ctx.respond("Check your DMs.")
        else:
            await ctx.respond("All commands are slash commands.")

def setup(client):
    client.add_cog(helpCommands(client))

# Make shitbot sometimes repost a message in a random other place
# Send DM's to people randomly telling them to go to a specific location
