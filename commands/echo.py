import discord
from discord.ext import commands

class echo(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def echo(self, ctx, *, thing):
        await ctx.send(thing)

def setup(client):
    client.add_cog(echo(client))