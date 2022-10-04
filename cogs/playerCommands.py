import discord
import json
import asyncio
from datetime import datetime
from datetime import timedelta
from discord.commands import slash_command
from discord.ext import commands


# Locks everyone but mods out
def onlyMods(ctx):
    modRole = discord.utils.get(ctx.author.guild.roles, name="Moderator/character")
    return modRole in ctx.author.roles


#slash_command_guilds = [925123755175460865, 709206749378248716, 960997598594994186]


class playerCommands(commands.Cog):
    def __init__(self, client):
        self.client = client
        print("Loaded playerCommands")

    @commands.command()
    async def test(self):
        print("tested")

    # Allows the user to bite another player
    @slash_command(guild_ids=[925123755175460865, 709206749378248716, 960997598594994186], name="bite", description="Bites a certain user.")
    async def bite(self, ctx, playerid, fed: discord.Member = None):
        with open('players.json', 'r') as f:
            save = json.load(f)
        with open('data.json', 'r') as f:
            points = json.load(f)

        # Checks to make sure the author is not a human or a starved zombie
        if save[str(ctx.author.id)]["Role"] == "Human":
            await ctx.respond("You are a human, humans do not bite people.")
            return
        if save[str(ctx.author.id)]["Starve Timer"] == "Starved":
            await ctx.respond("Starved zombies may not bite humans.")
            return

        # Loops through the players in players.json and finds the ID
        for player in save:
            if str(playerid) == save[player]['ID']:
                if save[player]["Role"] == "Zombie":  # Makes sure target is not already a zombie
                    await ctx.send("They are already a zombie.")
                    return

                member = await ctx.guild.fetch_member(int(player))
                save[player]["Role"] = "Zombie"
                time = datetime.now()  # Gets the time now
                future_date = time + timedelta(days=2)  # Sets a future date that is two days ahead of the current time
                date_format = '%m/%d/%Y %H:%M:%S'  # String formatting for saving the date
                future_date_str = future_date.strftime(date_format)  # Saves the future time in the string format
                save[player]["Starve Timer"] = future_date_str
                if not points["Remembrance"]:  # If remembrance is not active delete the upgrade
                    save[str(member.id)]["Upgrade"] = ""
                # Set starve timer of the zombie that bit to the future date
                save[str(ctx.author.id)]["Starve Timer"] = future_date_str
                save[str(ctx.author.id)]["Points"] += 2

                # Replace the roles the user has on discord
                role = discord.utils.get(ctx.author.guild.roles, name="Human")
                await member.remove_roles(role)
                role = discord.utils.get(ctx.author.guild.roles, name="Zombie")
                await member.add_roles(role)

                await ctx.respond(f"{member.display_name} has been bitten!")

                # If a user is specified to be fed then set that zombie's starve timer for the future date
                if fed:
                    if save[str(fed.id)]["Role"] == "Zombie":
                        save[str(fed.id)]["Starve Timer"] = future_date_str

                with open('players.json', 'w') as f:
                    json.dump(save, f, indent=4)

                # Adjust the zombie's points
                with open('data.json', 'r') as f:
                    points = json.load(f)
                points["Zombies"] += 2
                with open('data.json', 'w') as f:
                    json.dump(points, f, indent=4)
                return
        # If the user was not found then the ID was invalid
        await ctx.respond("That is an invalid ID.")

    @slash_command(guild_ids=[925123755175460865, 709206749378248716, 960997598594994186], name="stun", description="stuns a zombie.")
    async def stun(self, ctx, stunned: discord.Member = None):
        with open('players.json', 'r') as f:
            players = json.load(f)

        # Check to make sure the user is not a zombie
        if players[str(ctx.author.id)]["Role"] == "Zombie":
            await ctx.respond("Only humans can stun.")
            return

        # Gives the author a point
        players[ctx.author.id]["Points"] += 1
        with open('players.json', 'w') as f:
            json.dump(players, f, indent=4)

        # Gives the human team a point
        with open('data.json', 'r') as f:
            points = json.load(f)
        points["Humans"] += 1
        with open('data.json', 'w') as f:
            json.dump(points, f, indent=4)

        # If the user specified someone to be stunned they will be notified when their starve timer is up
        if stunned is not None:
            await ctx.respond(f"{stunned.display_name} has been stunned.")

            await asyncio.sleep(600)
            if players[players[str(ctx.author.id)]["Upgrade"] == "Bruiser"]:  # If the user has the Bruiser upgrade double time
                await asyncio.sleep(600)

            await ctx.respond(f"{stunned.display_name} is no longer stunned.")
        else:  # If no user is specified then send a general message
            await ctx.respond("A zombie has been stunned.")

            await asyncio.sleep(600)
            if players[players[str(ctx.author.id)]["Upgrade"] == "Bruiser"]:  # If the user has the Bruiser upgrade double time
                await asyncio.sleep(600)

            await ctx.respond(f"The zombie stunned by {ctx.author.display_name} is no longer stunned.")

    # Send the user information about themselves
    @slash_command(guild_ids=[925123755175460865, 709206749378248716, 960997598594994186], name="identity_crisis", description="Resend you ID.")
    async def identityCrisis(self, ctx):
        with open('players.json', 'r') as f:
            save = json.load(f)
        info = save[str(ctx.author.id)]
        # If the user is a Zombie send them their starve timer as well if not, do not add that to the embed
        if info["Role"] == "Zombie":
            playerEmbed = discord.Embed(title=f"Data for {info['Name']}",
                                        description=f"**ID**: {info['ID']}\n"
                                                    f"**Role**: {info['Role']}\n"
                                                    f"**Upgrade**: {info['Upgrade']}\n"
                                                    f"**Starve Timer**: {info['Starve Timer']}")
            if ctx.author.avatar is not None:  # Checks that the user has a profile picture before setting that for the embed
                playerEmbed.set_thumbnail(url=ctx.author.avatar)
            await ctx.respond("Your info has been sent to your DMs.")
            await ctx.author.send(embed=playerEmbed)
        else:
            playerEmbed = discord.Embed(title=f"Data for {info['Name']}", description=f"**ID**: {info['ID']}\n"
                                                                                      f"**Role**: {info['Role']}\n"
                                                                                      f"**Upgrade**: {info['Upgrade']}")
            if ctx.author.avatar is not None:  # Checks that the user has a profile picture before setting that for the embed
                playerEmbed.set_thumbnail(url=ctx.author.avatar)
            await ctx.respond("Your info has been sent to your DMs.")
            await ctx.author.send(embed=playerEmbed)

    # Returns a specified upgrade or returns the list of upgrades
    @slash_command(guild_ids=[925123755175460865, 709206749378248716, 960997598594994186], name="upgrade_lookup", description="Looks up information about a specified upgrade.")
    async def upgradeLookup(self, ctx, *, upgrade="Get List"):
        with open('upgrades.json', 'r', encoding='utf-8') as f:
            upgrades = json.load(f)

        # If the upgrade specified is Get List then print all keys
        if upgrade == "Get List":
            upgrades.keys()
            result = ""
            for i, key in enumerate(upgrades):
                result += f"{i + 1}. {key.title()} \n"

            myEmbed = discord.Embed(title="The upgrades you can look up are:", description=result, color=0x800080)
            myEmbed.set_footer(text="Use /upgrade_lookup [Name of upgrade] to see the description.")
            await ctx.respond(embed=myEmbed)
            return

        if upgrade.lower() in upgrades:
            myEmbed = discord.Embed(title=upgrade.title(), description=upgrades[upgrade.lower()], color=0x800080)
            await ctx.respond(embed=myEmbed)
        else:
            await ctx.respond("That's not an upgrade. Please try again, or don't that's up to you.")

    # returns all rules that
    @slash_command(guild_ids=[925123755175460865, 709206749378248716, 960997598594994186], name="rule_lookup",
                    description="Looks up information about any rule with the keyword.")
    async def ruleLookup(self, ctx, *, keyword="Get List"):
        with open('rules.json', 'r') as f:
            rules = json.load(f)

        await ctx.respond("This command has not yet been implemented. Want to help? DM Kira.")


def setup(client):
    client.add_cog(playerCommands(client))
