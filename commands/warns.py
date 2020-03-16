import discord
from discord.ext import commands

def Convert(string): 
    li = list(string.split("-")) 
    return li 

class warns(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def warns(self, ctx, user : discord.Member = None):
        f = open("warnings.txt", "r")
        list_ = Convert(f.read())
        warns = 0

        if user == None:
            if not(f == ""):
                for i in list_:
                    if i.split(":")[0] == str(ctx.author.id):
                        warns = int(i.split(":")[1])
                        break
            await ctx.send(f"You've got **{warns}** warnings!")
        else:
            if not(f == ""):
                for i in list_:
                    if i.split(":")[0] == str(user.id):
                        warns = int(i.split(":")[1])
                        break
            await ctx.send(f"{user.name} has got **{warns}** warnings!")
        
    @warns.error
    async def warns_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send(":x: Please specify an existing user!")

def setup(client):
    client.add_cog(warns(client))