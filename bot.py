from datetime import datetime

import discord
import json
import os
from discord.ext import commands, tasks

# Prefix for messages
intents = discord.Intents().all()
bot = commands.Bot(command_prefix="$", intents=intents)
bot.remove_command("help")


@bot.command()
@commands.has_permissions(administrator=True)
async def load(ctx, extension):
    await bot.load_extension(f"cogs.{extension}")
    await ctx.message.add_reaction(emoji='✅')


@bot.command()
@commands.has_permissions(administrator=True)
async def unload(ctx, extension):
    await bot.unload_extension(f"cogs.{extension}")
    await ctx.message.add_reaction(emoji='✅')


@bot.command()
@commands.has_permissions(administrator=True)
async def reload(ctx, extension):
    await bot.unload_extension(f"cogs.{extension}")
    await bot.load_extension(f"cogs.{extension}")
    await ctx.message.add_reaction(emoji='✅')


@tasks.loop(seconds=60)
async def checkStarve():
    getTime = datetime.now()
    date_format = '%m/%d/%Y %H:%M:%S'
    curTime = getTime.strftime(date_format).split()
    print(f"Beginning Check {curTime}")

    with open('players.json', 'r') as f:
        players = json.load(f)

    for player in players:
        if players[player]["Role"] == "Human":
            continue
        else:
            playerTime = (players[player]["Starve Timer"]).split()
            if playerTime[0] == curTime[0]:
                if int(playerTime[1][0:2]) < int(curTime[1][0:2]):
                    players[player]["Starve Timer"] = "Starved"
                    starve_channel = bot.get_channel(1122499753222090755)
                    user = await bot.fetch_user(player)
                    await starve_channel.send(f"{user.display_name} has starved!")

                elif int(playerTime[1][0:2]) == int(curTime[1][0:2]) and int(playerTime[1][3:5]) < int(curTime[1][3:5]):
                    players[player]["Starve Timer"] = "Starved"
                    starve_channel = bot.get_channel(1122499753222090755)
                    user = await bot.fetch_user(player)
                    await starve_channel.send(f"{user.display_name} has starved!")

    with open('players.json', 'w') as f:
        json.dump(players, f, indent=4)

    getTime = datetime.now()
    date_format = '%m/%d/%Y %H:%M:%S'
    curTime = getTime.strftime(date_format).split()
    print(f"Check Complete {curTime}")


@tasks.loop(count=1)
async def wait_until_ready():
    await bot.wait_until_ready()
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("Use /help"))
    if not checkStarve.is_running():
        checkStarve.start()
    await load_extentions()



async def load_extentions():
    for filename in os.listdir('./cogs'):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")


async def main():
    wait_until_ready.start()
    print("bot is up and running.")
    await bot.start("OTI1OTU5NTE4MjM0NDc2NjI1.GurD_q.yc2x4vOozLTSFJsOcpJS4Is_0JAsPSMV2vEGxE")



if __name__ == '__main__':
    import asyncio

    asyncio.run(main())

