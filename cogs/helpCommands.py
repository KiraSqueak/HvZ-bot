import discord, json
from discord.ext import commands


class helpCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Returns a list of commands available
    @commands.command()
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
            myEmbed.set_author(name="Hvzbot")
            await ctx.author.send(embed=myEmbed)
            await ctx.send("Check your DMs.")
        else:
            myEmbed = discord.Embed(title="Mod Command List", description="<> = required field    [] = optional field",
                                    color=0x800080)
            myEmbed.add_field(name="Bite", value="Bites a human. Format: $bite <user ID> [mention user to feed]",
                              inline=False)
            myEmbed.add_field(name="Stun", value="Stuns a zombie. Format: $stun [mention user stunned]",
                              inline=False)
            myEmbed.add_field(name="Identity Crisis", value="Sends you your ID again. Format: $identityCrisis",
                              inline=False)
            myEmbed.add_field(name="Upgrade Lookup", value="Looks up the description of an upgrade. Format: $upgradeLookup [name of upgrade]",
                              inline=False)
            myEmbed.set_author(name="Hvzbot")
            await ctx.send(embed=myEmbed)


async def setup(client):
    await client.add_cog(helpCommands(client))

# Send DM's to people randomly telling them to go to a specific location
