import discord
from discord.ext import commands

class ban(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user : discord.Member, *, reason = "Not specified"):
        if user.guild_permissions.administrator:
            await ctx.send(":x: You can't ban this user.")
            return

        await ctx.send(embed=discord.Embed(
            title = "Success!",
            description = f":white_check_mark: You've banned {user} from this server!\nReason: **{reason}**",
            colour = discord.Colour.green()
        ))

        #Log

        log_channel = ""
        for channel in ctx.guild.channels:
            if channel.name == "logs":
                log_channel = channel
                break

        if log_channel == "":
            await ctx.send(":x: Couldn't find `#logs` channel. Please create one!")
        
        await log_channel.send(embed=discord.Embed(
            title = "Banned User",
            description = f"<@{ctx.author.id}> has banned {user}.\nReason: {reason}",
            colour = discord.Colour.red()
        ))

        await user.ban(reason=f"{ctx.author} have banned you from {ctx.channel.guild.name}. Reason: {reason}")
        await user.send(reason=f"{ctx.author} have banned you from {ctx.channel.guild.name}. Reason: {reason}")

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(":x: You don't have permission to run this command!")
        if isinstance(error, commands.BadArgument):
            await ctx.send(":x: Please specify an existing user!")

def setup(client):
    client.add_cog(ban(client))