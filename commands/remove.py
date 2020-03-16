import discord
from discord.ext import commands

class remove(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def remove(self, ctx, user : discord.Member = None):
        if not("ticket" in ctx.channel.name):
            await ctx.send(":x: You can only run this command in a ticket channel")
            return

        if user is None:
            return await ctx.send(":x: Please mention a user!")

        if not(user in ctx.channel.members):
            return await ctx.send(":x: This member has no permissions to this ticket.")

        channel = ctx.channel
        await channel.set_permissions(user, read_messages=False)
        await ctx.send(f":white_check_mark: I've removed <@{user.id}> from this ticket!")


    @remove.error
    async def remove_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(":x: You don't have permission to run this command!", delete_after=5.0)
        if isinstance(error, discord.ext.commands.BadArgument):
            await ctx.send(":x: Please specify an existing user")

def setup(client):
    client.add_cog(remove(client))