import discord
from discord.ext import commands

def Convert(string): 
    li = list(string.split("-")) 
    return li 

class warn(commands.Cog):

    def __init___(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def warn(self, ctx, user : discord.Member, *, reason = "Not specified"):
        if user == ctx.author:
            return await ctx.send(":x: C'mon, you can't warn yourself..")


        fr_ = open("warnings.txt", "r")
        fr = fr_.read()
        fw = open("warnings.txt", "w")
        list_ = Convert(fr)

        if not(fr == ""):
            if not(str(user.id) in list_):
                list_.append(str(user.id) + ":0")
        else:
            list_.append(str(user.id) + ":0")
            del list_[0]
        print(list_)

        
        warns = 0
        index = 0
        for i in list_:
            print("asd")
            if user.id == int(i.split(":")[0]):
                warns = int(i.split(":")[1])
                index = list_.index(i)
                break
            

        warns += 1
        if warns == 3:
            await ctx.send(embed=discord.Embed(
                title = "Success!",
                description = f":white_check_mark: You've successfully warned {user}, and they've reached 3 warnings so they've got kicked!",
                colour = discord.Colour.green()
            ))
            del list_[index]
            await user.kick(reason=f"You've been warned by: {ctx.author}. You've reached 3 warnings, so you've been kicked out of the server.")
            await user.send(reason=f"You've been warned by: {ctx.author}. You've reached 3 warnings, so you've been kicked out of the server.")
        else:
            await ctx.send(embed=discord.Embed(
                title = "Success!",
                description = f":white_check_mark: You've successfully warned {user}!\nThis member's got **{warns}** warnings!",
                colour = discord.Colour.green()
            ))
            await user.send(f":warning: You've been warned by: {ctx.author}. Reason: **{reason}**")

        list_[index] = str(user.id) + ":" + str(warns)

        last_string = ""
        for i in list_:
            last_string += i + "-\n"
        fw.write(last_string)
        fw.close()

    @warn.error
    async def warn_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(":x: You don't have permission to run this command!")
        if isinstance(error, commands.BadArgument):
            await ctx.send(":x: Please specify an existing user!")

def setup(client):
    client.add_cog(warn(client))