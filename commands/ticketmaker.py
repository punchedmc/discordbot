import json
import discord
from discord.ext import commands

class ticketmaker(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot ready!")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def ticket_maker(self, ctx):
        embed = discord.Embed(
            title = 'Make a ticket',
            description = "Choose what you need help with by reacting with the correct emoji\n" + 
                        "Available requests:\n" +
                            ":orange_circle: Player Report\n" + 
                            ":green_circle: Billing Support\n" +
                            ":red_circle: Server Report\n" +
                            ":blue_circle: Staff Report\n" +
                            ":purple_circle: Other\n" +
                            "\nOr if you'd like to make an appeal, react with 👮",
            colour = discord.Colour.blue()
        )

        msg = await ctx.send(embed=embed)
        await msg.add_reaction("🟠")
        await msg.add_reaction("🟢")
        await msg.add_reaction("🔴")
        await msg.add_reaction("🔵")
        await msg.add_reaction("🟣")
        await msg.add_reaction("👮")

        data = {
            "messageID": msg.id
        }

        with open("messageID.json", "w") as outfile:
            json.dump(data, outfile)

    @ticket_maker.error
    async def ticketmaker_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(":x: You don't have permission to run this command!", delete_after=5.0)


def setup(client):
    client.add_cog(ticketmaker(client))


