import discord
from discord.ext import commands

class kick(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user : discord.Member = None, *, reason = "Not specified"):
        if user.guild_permissions.administrator:
            await ctx.send(":x: You can't kick this user.")
            return

        await ctx.send(embed=discord.Embed(
            title = "Success!",
            description = f":white_check_mark: You've kicked {user} from this server!\nReason: **{reason}**",
            colour = discord.Colour.green()
        ))
        await user.kick(reason=f"{ctx.author} have kicked you out of {ctx.channel.guild.name}. Reason: {reason}")
        await user.send(f"{ctx.author} have kicked you out of {ctx.channel.guild.name}. Reason: {reason}")

        log_channel = ""
        for channel in ctx.guild.channels:
            if channel.name == "logs":
                log_channel = channel
                break

        if log_channel == "":
            await ctx.send(":x: Couldn't find `#logs` channel. Please create one!")
        
        await log_channel.send(embed=discord.Embed(
            title = "Kicked User",
            description = f"<@{ctx.author.id}> has kicked {user}.\nReason: {reason}",
            colour = discord.Colour.orange()
        ))

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(":x: You don't have permission to run this command!")
        if isinstance(error, commands.BadArgument):
            await ctx.send(":x: Please specify an existing user!")

def setup(client):
    client.add_cog(kick(client))