import discord
from discord.ext import commands

def check(author):
    def inner_check(message): 
        if message.author != author:
            return False
        try: 
            if message.content == "CONFIRM":
                return True 
        except ValueError: 
            return False
    return inner_check

class close(commands.Cog):
    
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def close(self, ctx):
        await ctx.send(embed=discord.Embed(
            title = ":warning: Confirmation",
            description = "This channel is going to be deleted!\n**Type 'CONFIRM' in 10 seconds to confirm the deleting process!**",
            colour = discord.Colour.orange()
        ))
        reply = await self.client.wait_for('message', check=check(ctx.author), timeout=10)
        if reply.content == "CONFIRM":
            await ctx.channel.delete()
            await ctx.author.send(f':white_check_mark: **{ctx.channel.split("-")[1]}"s** ticket has been successfully deleted!')
            

    @close.error
    async def close_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(":x: You don't have permission to run this command!", delete_after=5.0)


def setup(client):
    client.add_cog(close(client))