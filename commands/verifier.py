import discord
import json
from discord.ext import commands

class verifier(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def verifier(self, ctx):
        if not(ctx.channel.name == "verify"):
            await ctx.send(":x: You can only run this command in the #verify channel! If you haven't got one, make sure to create one!")

        verify_msg = await ctx.channel.send(embed=discord.Embed(
            title = "Verification | PunchedMC",
            description = "React below to receive member role and gain access to the server. If you can’t react please wait 10 minutes, if you still can’t react contact an Administrator.\n\n:white_check_mark: = Member (Verification Role)",
            colour = discord.Colour.blue()
        ))
        await verify_msg.add_reaction("✅")

        f = open("verifierID.txt", "w")
        f.write(str(verify_msg.id))
        f.close()

    @verifier.error
    async def verifier_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(":x: You don't have permission to run this command!")

def setup(client):
    client.add_cog(verifier(client))