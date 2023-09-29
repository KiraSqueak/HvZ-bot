import discord
import json
import random
import string
from discord.ext import commands


class createServer(commands.Cog):
    def __init__(self, client):
        self.client = client


async def setup(client):
    await client.add_cog(createServer(client))
