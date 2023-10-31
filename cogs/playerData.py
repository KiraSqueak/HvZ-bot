from datetime import datetime
from datetime import timedelta

import discord
import json
from discord.ext import commands


# Locks everyone but mods out
def onlyMods(ctx):
    modRole = discord.utils.get(ctx.author.guild.roles, name="Moderator/character")
    return modRole in ctx.author.roles


class playerData(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Prints all registered users
    @commands.command()
    @commands.check(onlyMods)
    async def printy(self, ctx):
        with open('players.json', 'r') as f:
            save = json.load(f)
        if len(save) > 0:
            await ctx.send("Sending all users data:")
            for info in save:
                playerEmbed = discord.Embed(title=f"Data for {save[info]['Name']}",
                                            description=f"**ID**: {save[info]['ID']}\n"
                                                        f"**Role**: {save[info]['Role']}\n"
                                                        f"**Upgrade**: {save[info]['Upgrade']}\n"
                                                        f"**Starve Timer**: {save[info]['Starve Timer']}\n"
                                                        f"**Points**: {save[info]['Points']}")
                await ctx.send(embed=playerEmbed)
        else:
            await ctx.send("There are no players registered.")

    # Gets the data of a specified user
    @commands.command()
    @commands.check(onlyMods)
    async def getData(self, ctx, member: discord.Member = None):
        with open('players.json', 'r') as f:
            save = json.load(f)
        info = save[str(member.id)]
        playerEmbed = discord.Embed(title=f"Data for {info['Name']}",
                                    description=f"**ID**: {info['ID']}\n"
                                                f"**Role**: {info['Role']}\n"
                                                f"**Upgrade**: {info['Upgrade']}\n"
                                                f"**Starve Timer**: {info['Starve Timer']}\n"
                                                f"**Points**: {info['Points']}")
        if member.avatar is not None:  # Checks that the user has a profile picture before setting that for the embed
            playerEmbed.set_thumbnail(url=member.avatar)
        await ctx.send(embed=playerEmbed)

    # Mod bites the user with the ID, no points are earned.
    @commands.command()
    @commands.check(onlyMods)
    async def modBite(self, ctx, playerid):
        with open('players.json', 'r') as f:
            save = json.load(f)
        with open('data.json', 'r') as f:
            points = json.load(f)

        # Searches through the players.json file for the correct ID
        for player in save:
            if str(playerid) == save[player]['ID']:
                if save[player]["Role"] == "Zombie":  # Makes sure the user in not already a zombie
                    await ctx.send("They are already a zombie.")
                    return

                member = await ctx.guild.fetch_member(int(player))  # Gets the member from the ID
                save[player]["Role"] = "Zombie"
                time = datetime.now()  # Gets the time now
                future_date = time + timedelta(days=2)  # Sets a future date that is two days ahead of the current time
                date_format = '%m/%d/%Y %H:%M:%S'  # String formatting for saving the date
                future_date_str = future_date.strftime(date_format)  # Saves the future time in the string format
                save[player]["Starve Timer"] = future_date_str
                if not points["Remembrance"]:  # If remembrance is not active delete the upgrade
                    save[str(member.id)]["Upgrade"] = ""

                # Replace the roles the user has on discord
                role = discord.utils.get(ctx.author.guild.roles, name="Human")
                await member.remove_roles(role)
                role = discord.utils.get(ctx.author.guild.roles, name="Zombie")
                await member.add_roles(role)

                with open('players.json', 'w') as f:
                    json.dump(save, f, indent=4)

                await ctx.send(f"{member.display_name} has been bitten!")
                return

        await ctx.send("Invalid ID")

    # Mod command to unbite a user and remove the points from the zombies
    @commands.command()
    @commands.check(onlyMods)
    async def unbite(self, ctx, member: discord.Member = None):
        with open('data.json', 'r') as f:
            points = json.load(f)
        points["Zombies"] -= 2  # Removing the points
        with open('data.json', 'w') as f:
            json.dump(points, f, indent=4)

        with open('players.json', 'r') as f:
            save = json.load(f)
        save[str(member.id)]["Role"] = "Human"
        save[str(member.id)]["Starve Timer"] = -1
        save[str(member.id)]["Upgrade"] = ""

        # Replace the roles the user has on discord
        role = discord.utils.get(ctx.author.guild.roles, name="Zombie")
        await member.remove_roles(role)
        role = discord.utils.get(ctx.author.guild.roles, name="Human")
        await member.add_roles(role)

        with open('players.json', 'w') as f:
            json.dump(save, f, indent=4)

        await ctx.send(f"{member.display_name} has been cured and 2 points have been taken from the zombie team.")

    # Cures a zombie but does not remove points
    @commands.command()
    @commands.check(onlyMods)
    async def cure(self, ctx, member: discord.Member = None):
        with open('players.json', 'r') as f:
            save = json.load(f)

        save[str(member.id)]["Role"] = "Human"
        save[str(member.id)]["Starve Timer"] = -1
        save[str(member.id)]["Upgrade"] = ""

        # Replace the roles the user has on discord
        role = discord.utils.get(ctx.author.guild.roles, name="Zombie")
        await member.remove_roles(role)
        role = discord.utils.get(ctx.author.guild.roles, name="Human")
        await member.add_roles(role)

        with open('players.json', 'w') as f:
            json.dump(save, f, indent=4)

        await ctx.send(f"{member.display_name} has been cured.")

    # Sets starve timers of all zombies to two days in the future
    @commands.command()
    @commands.check(onlyMods)
    async def feast(self, ctx):
        with open('players.json', 'r') as f:
            players = json.load(f)

        time = datetime.now()  # Gets the current time
        future_date = time + timedelta(days=2)  # Sets a future date that is two days ahead of the current time
        date_format = '%m/%d/%Y %H:%M:%S'  # String formatting for saving the date
        future_date_str = future_date.strftime(date_format)  # Saves the future time in the string format

        # Updates all not starved zombies with the new starve timer
        for player in players:
            if players[player]["Role"] == "Human" or (
                    players[player]["Role"] == "Zombie" and players[player]["Starve Timer"] == "Starved"):
                continue
            else:
                players[player]["Starve Timer"] = future_date_str

        with open('players.json', 'w') as f:
            json.dump(players, f, indent=4)

    # Adds an upgrade to a user
    @commands.command()
    @commands.check(onlyMods)
    async def addUpgrade(self, ctx, member: discord.Member, *, upgrade):
        with open('data.json', 'r') as f:
            points = json.load(f)
        # If the upgrade being changed is Remembrance change it in data not for a player
        if upgrade == "Remembrance":
            points["Remembrance"] = True
            with open('data.json', 'w') as f:
                json.dump(points, f, indent=4)
            return

        # Add the upgrade to the mentioned user
        with open('players.json', 'r') as f:
            players = json.load(f)

        players[str(member.id)]["Upgrade"] = upgrade.title()

        with open('players.json', 'w') as f:
            json.dump(players, f, indent=4)

        await ctx.send(f"Upgrade {upgrade.title()} has been added to {member.display_name}")


async def setup(client):
    await client.add_cog(playerData(client))
