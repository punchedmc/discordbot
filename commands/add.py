import discord
from discord.ext import commands

class add(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def add(self, ctx, user : discord.Member = None):
        if not(ctx.channel.name.split("-")[0] == "ticket"):
            await ctx.send(":x: You can only run this command in a ticket channel")
            return

        if user is None:
            return await ctx.send(":x: Please mention a user!")

        print(ctx.channel.members)
        if user in ctx.channel.members:
            return await ctx.send(":x: This member is already has permissions to this ticket!")

        await ctx.channel.set_permissions(user, read_messages=True)
        print("asd")
        await ctx.send(f":white_check_mark: I've added <@{user.id}> into this ticket!")


    @add.error
    async def add_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(":x: You don't have permission to run this command!", delete_after=5.0)
        if isinstance(error, discord.ext.commands.BadArgument):
            await ctx.send(":x: Please specify an existing user")

def setup(client):
    client.add_cog(add(client))