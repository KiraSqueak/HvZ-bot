import random
import traceback as tb

from discord.ext import commands


class Events(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Give me the information I need then I can do what you want.")
        elif isinstance(error, commands.CommandNotFound):
            await ctx.send("That's not even a command.")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("You are not allowed to do that.")
        elif isinstance(error, commands.CheckFailure):
            await ctx.send("You are not allowed to do that.")
        else:
            await ctx.send(error)
            print('\n'.join(tb.format_exception(None, error, error.__traceback__)))

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == 784421124779933707:
            return
        if "hvzbot" in message.content.lower() and random.randint(0, 10) == 5:
            general_channel = self.client.get_channel(message.channel.id)
            await general_channel.send("*Peeks around corner.*")
        if "how are you" in message.content.lower() and "shitbot" in message.content.lower():
            general_channel = self.client.get_channel(message.channel.id)
            await general_channel.send("Better than you.")
        if "ID" in message.content and random.randint(0, 10) == 5:
            general_channel = self.client.get_channel(message.channel.id)
            await general_channel.send("***NO***")
        if random.randint(0, 500) == -225:
            general_channel = self.client.get_channel(message.channel.id)
            special = ["I have a question.", "Urgent situation!", "There is a flaw in your logic.",
                       "Repeat that slowly.", "You...", "I look forward to your demise.", "This should be good.",
                       "How long till you die I wonder?",
                       "May all your teeth fall out but one so you may still get a tooth ache.",
                       "May you be so rich your widow's husband never has to work a day.",
                       "May you have the most comfortable mattress and one thousand sleepless nights.",
                       "Stay healthy so you can kill yourself later.", "Let him suffer and remember.",
                       "Dumkopf", "May you be so enamored of good food that you turn into a mouse, and may your enemy "
                                  "turn into a cat, and may he eat you up and choke on you, so we can be rid of you "
                                  "both."]
            await general_channel.send(random.choice(special))


async def setup(client):
    await client.add_cog(Events(client))
