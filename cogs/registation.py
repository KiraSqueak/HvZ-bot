import discord
import json
import random
import string
from discord.ext import commands


# Locks everyone but mods out
def onlyMods(ctx):
    modRole = discord.utils.get(ctx.author.guild.roles, name="Moderator/character")
    return modRole in ctx.author.roles


class registration(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Generates a random id for the player
    async def generateNumber(self):
        with open('players.json', 'r') as f:
            save = json.load(f)
        chars = string.ascii_uppercase + string.digits
        generated = ''.join(random.choice(chars) for _ in range(5))
        while generated in save:
            print("THIS TRIGGERED!")
            for num in range(5):
                generated += chr(random.randint(48, 90))
        return generated

    # Registers all players for the game
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def register(self, ctx):
        await ctx.send("Beginning the registration of players!")
        save = {}
        for member in ctx.guild.members:
            # Adds the three roles that should be ignored by shitbot
            modRole = discord.utils.get(ctx.author.guild.roles, name="Moderator/character")
            NPCRole = discord.utils.get(ctx.author.guild.roles, name="NPC")
            BotRole = discord.utils.get(ctx.author.guild.roles, name="Bot")
            # If the role of the user is not one of the roles to be ignored then register them
            if modRole not in member.roles and NPCRole not in member.roles and BotRole not in member.roles:
                id = await self.generateNumber() # Generates a unique id for the user
                save[member.id] = {'Name': member.display_name,
                                   'ID': id,
                                   'Role': 'Human',
                                   'Upgrade': "",
                                   'Starve Timer': -1,
                                   "Points": 0}
                role = discord.utils.get(ctx.author.guild.roles, name="Human")
                await member.add_roles(role)
                # Attempts to send the id to the user, may fail if the used does not accept DMs from people in the same guild
                try:
                    await member.send(f"Your ID is: {id}")
                except:
                    print(f"Failed sending ID to {member.display_name}")

            print(f"Registered {member.display_name}")

        with open('players.json', 'w') as f:
            json.dump(save, f, indent=4)

        await ctx.send("All players registered! Let the hunt begin!")

    # Adds a user to the game after register has been called
    @commands.command()
    @commands.check(onlyMods)
    async def induct(self, ctx, member: discord.Member = None):
        with open('players.json', 'r') as f:
            save = json.load(f)

        id = await self.generateNumber()  # Generate the user a random ID
        save[member.id] = {'Name': member.display_name,
                           'ID': id,
                           'Role': 'Human',
                           'Upgrade': "",
                           'Starve Timer': -1,
                           'Points': 0}
        role = discord.utils.get(ctx.author.guild.roles, name="Human")
        await member.add_roles(role)
        # Attempts to send the id to the user, may fail if the used does not accept DMs from people in the same guild
        try:
            await member.send(f"Your ID is: {id}")
        except:
            print(f"Failed sending ID to {member.display_name}")

        with open('players.json', 'w') as f:
            json.dump(save, f, indent=4)

        await ctx.send(f"{member.display_name} has entered the fray.")

    # Clears all data from the players and data json files
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def clearData(self, ctx):
        with open('players.json', 'w') as f:
            json.dump({}, f, indent=4)
        save = {"Humans": 0, "Zombies": 0, "Remembrance": False}
        with open('data.json', 'w') as f:
            json.dump(save, f, indent=4)

        await ctx.send("All data cleared.")


def setup(client):
    client.add_cog(registration(client))
