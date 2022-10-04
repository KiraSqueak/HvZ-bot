import discord
import json
from discord.ext import commands


# Locks everyone but mods out
def onlyMods(ctx):
    modRole = discord.utils.get(ctx.author.guild.roles, name="Moderator/character")
    return modRole in ctx.author.roles


class pointsCommands(commands.Cog):
    def __init__(self, client):
        self.client = client
        print("Loaded points Commands")

    # Adds points to the specified team
    @commands.command()
    @commands.check(onlyMods)
    async def addPoints(self, ctx, team, amount):
        with open('data.json', 'r') as f:
            points = json.load(f)
        points[team] += int(amount)
        with open('data.json', 'w') as f:
            json.dump(points, f, indent=4)

        await ctx.send(f"Team {team} has had {amount} points added.")

    # Removes points from the specified team
    @commands.command()
    @commands.check(onlyMods)
    async def removePoints(self, ctx, team, amount):
        with open('data.json', 'r') as f:
            points = json.load(f)
        points[team] -= int(amount)
        if (points[team] < 0):
            points[team] = 0
        with open('data.json', 'w') as f:
            json.dump(points, f, indent=4)
        await ctx.send(f"Team {team} has had {amount} points removed.")

    # Adds points from the specified Player
    @commands.command()
    @commands.check(onlyMods)
    async def addPlayerPoints(self, ctx, member: discord.Member, amount):
        with open('players.json', 'r') as f:
            players = json.load(f)
        players[str(member.id)]["Points"] += int(amount)
        with open('players.json', 'w') as f:
            json.dump(players, f, indent=4)
        await ctx.send(f"User {member.display_name} has had {amount} points added.")

    # Removes points from the specified player
    @commands.command()
    @commands.check(onlyMods)
    async def removePlayerPoints(self, ctx, member: discord.Member, amount):
        with open('players.json', 'r') as f:
            players = json.load(f)
        players[str(member.id)]["Points"] -= int(amount)
        if players[str(member.id)]["Points"] < 0:
            players[str(member.id)]["Points"] = 0
        with open('players.json', 'w') as f:
            json.dump(players, f, indent=4)
        await ctx.send(f"User {member.display_name} has had {amount} points removed.")

    # Displays the points of both teams
    @commands.command()
    @commands.check(onlyMods)
    async def displayPoints(self, ctx):
        with open('data.json', 'r') as f:
            points = json.load(f)
        playerEmbed = discord.Embed(title="Points:",
                                    description=f"**Humans**: {points['Humans']}\n**Zombies**: {points['Zombies']}")
        await ctx.send(embed=playerEmbed)


def setup(client):
    client.add_cog(pointsCommands(client))
