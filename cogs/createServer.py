import discord
import json
import random
import string
from discord.ext import commands
from discord.commands import slash_command


class createServer(commands.Cog):
    def __init__(self, client):
        self.client = client




def setup(client):
    client.add_cog(createServer(client))
