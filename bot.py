import discord
import os
import json
from discord.ext import commands

#Prefix setting
client = commands.Bot(command_prefix=">")
client.remove_command("help") #This is an already existing command, basically, if I remove it, I can make my own help command

@client.event
async def on_ready():
    print("Ready!")
    await client.change_presence(activity=discord.Game(name="PunchedMC!"))

#Load a command
@client.command()
async def load(ctx, extension):
    client.load_extension(f'commands.{extension}')

#Unload a command
@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'commands.{extension}')

for filename in os.listdir('./commands'):
    if filename.endswith('.py'):
        client.load_extension(f'commands.{filename[:-3]}')

@client.command()
async def ping(ctx):
    await ctx.send(":ping_pong: Pong! **{0}ms**".format(round(client.latency * 1000)))

# rly gud command :)
@client.command()
async def clearthisshit(ctx):
    for channel in ctx.guild.channels:
        if channel.name == "ticket-watto":
            await channel.delete()

@client.event
async def on_member_join(member):
    welcome_channel = ""
    for channel in member.guild.channels:
        if channel.name == "new-members":
            welcome_channel = channel
            break
    
    if welcome_channel == None:
        print("Couldn't find welcome channel!")
    
    await welcome_channel.send(embed=discord.Embed(
        title = "Welcome to the server!",
        description = f"Welcome <@{member.id}> to the PunchedMC Discord!\n\n" +
                    ":small_red_triangle_down: Information :small_red_triangle_down:\n" +
                    ":white_small_square:  IP ➟ punchedmc.com\n" +
                    ":white_small_square:  Store ➟ https://store.punchedmc.com/\n" +
                    ":white_small_square:  Website ➟ https://punchedmc.com/",
        colour = discord.Colour.blue()
    ))


#Making a ticket process
@client.event
async def on_reaction_add(reaction, user): 
    f1 = open("messageID.json", "r")
    if user.bot:
        return
    if user == client.user:
        return

    #Ticket maker
    data = json.load(f1)
    messageid = data["messageID"]
    if reaction.message.id == messageid:
        await reaction.message.remove_reaction(reaction,user)
        if reaction.emoji == "🟠": #Player Report
            await create_ticket("Player Report", reaction.message.guild, user)
        elif reaction.emoji == "🟢": #Billing Support
            await create_ticket("Billing Support", reaction.message.guild, user)
        elif reaction.emoji == "🔴": #Server Report
            await create_ticket("Server Report", reaction.message.guild, user)
        elif reaction.emoji == "🔵": #Staff Report
            await create_ticket("Staff Report", reaction.message.guild, user)
        elif reaction.emoji == "🟣": #Other
            await create_ticket("Other", reaction.message.guild, user)
        elif reaction.emoji == "👮": #Appeal
            await create_appeal(reaction.message.guild, user)

    #Verification
    vid_f = open("verifierID.txt", "r")
    vid = int(vid_f.read())
    if reaction.message.id == vid:
        if reaction.emoji == "✅":
            verified_role = ""
            for r in reaction.message.guild.roles:
                if r.name == "Member":
                    verified_role = r
                    break
            
            if verified_role == "":
                return await user.send(":x: Couldn't find Member role. Please contact an Administrator!")

            await reaction.message.remove_reaction(reaction, user)
            await user.add_roles(verified_role)

    #Staff assignment
    f_ = open("new_ticket_ids.txt", "r")
    f = f_.read()
    list_ = Convert(f)
    for index in list_:
        current1 = index.replace("\n", "")
        current = current1.split(":")
        if current[0] == str(reaction.message.id):
            channel_id = int(current[1])
            ticket_ch = client.get_channel(channel_id)
            if ticket_ch is None:
                await reaction.message.channel.send(":x: This channel no longer exists!")
                return
            ticket_name = ticket_ch.name.split("-")[1]

            mention_user = f"<@{user.id}>"
            new_embed = discord.Embed(
                title = "Claimed ticket",
                description = f"{ticket_name}'s ticket has been claimed by: {mention_user}",
                colour = discord.Colour.green()
            )
            await reaction.message.edit(embed=new_embed)
            await reaction.message.clear_reactions()
            
            claimed_ticket = discord.Embed(
                title = "A staff member has been assigned to your ticket!",
                description = f"{mention_user} is handling your ticket for you.",
                colour = discord.Colour.green()
            )
            await ticket_ch.set_permissions(user, read_messages=True)
            await ticket_ch.send(embed=claimed_ticket)
            break

    #Appeal
    f2_ = open("new_appeal_ids.txt", "r")
    f2 = f2_.read()
    list2_ = Convert(f2)
    for index in list2_:
        current2 = index.replace("\n", "")
        if current2 == "":
            return
            
        if int(current2) == reaction.message.id:
            appealer = reaction.message.guild.get_member(int(reaction.message.embeds[0].description.split(">")[0].replace("<@","")))
            if appealer == None:
                return await user.send("An error occurred while managing an appeal: **Couldn't find user.**")

            if reaction.emoji == "✅":
                await appealer.send(embed=discord.Embed(
                    title = "",
                    description = f":white_check_mark: Your appeal got approved by {user}! Please allow up to 24hours for someone to remove your punishment",
                    colour = discord.Colour.green()
                ))

                await user.send(embed=discord.Embed(
                    title = "",
                    description = f":white_check_mark: Successfully approved {appealer}'s appeal!",
                    colour = discord.Colour.green()
                ))

                await reaction.message.edit(embed=discord.Embed(
                    title = "Approved Appeal",
                    description = f"<@{appealer.id}>'s appeal has been accepted :white_check_mark:\nAccepted by: <@{user.id}>",
                    colour = discord.Colour.green()
                ))
            elif reaction.emoji == "❌":
                await appealer.send(embed=discord.Embed(
                    description=f":x: Your appeal got denied by {user.name}",
                    colour = discord.Colour.red()))
                await user.send(embed=discord.Embed(
                    description = f":white_check_mark: Successfully denied {appealer}'s appeal!",
                    colour = discord.Colour.red()))
                await reaction.message.edit(embed=discord.Embed(
                    title = "Denied Appeal",
                    description = f"<@{appealer.id}>'s appeal has been denied. :x:\nDenied by: <@{user.id}>",
                    colour = discord.Colour.red()
                ))

            await reaction.message.clear_reactions()

            break

                

async def create_appeal(guild, creator):
    await creator.send(embed=discord.Embed(
        title = "Appeal",
        description = "Please fill out this form, and I'll make an appeal ticket for you! You'll have **5 minutes** to write your anwser at each question.\nIf you would like to cancel this process, type **'cancel'** anytime as anwser at any questions.",
        colour = discord.Colour.blue()
    ))

    def check(m):
        return m.author.id == creator.id

    ign = ""
    reason = ""
    length_of_p = ""
    punisher = ""
    reason_of_appeal = ""

    l = list(range(5))
    print(l)
    for i in l:
        description = ""
        if i == 0:
            description = "Please give me your IGN!"
        elif i == 1:
            description = "What was the reason that you've got your punishment?"
        elif i == 2:
            description = "What is the length of your punishment?"
        elif i == 3:    
            description = "Who punished you?"
        elif i == 4:
            description = "Why do you want to appeal?"

        msg = await creator.send(embed=discord.Embed(
            title = "Appeal",
            description = description,
            colour = discord.Colour.blue()
        ))

        reply1 = await client.wait_for('message', check=check, timeout=300)
        reply = reply1.content
        if reply.upper() == "CANCEL":
            await creator.send(":x: Cancelled!")
            return

        if i == 0:
            ign = reply
        elif i == 1:
            reason = reply
        elif i == 2:
            length_of_p = reply
        elif i == 3:    
            punisher = reply
        elif i == 4:
            reason_of_appeal = reply

    appeals_channel = ""
    for channel in guild.channels:
        if channel.name == "new-appeals":
            appeals_channel = channel
            break
    
    if appeals_channel == "":
        return await creator.send("**Missing'new-appeals' channel!** (send this message to a staff)")
    
    await creator.send(embed=discord.Embed(
        description=":white_check_mark: I've posted your appeal. The staff members are going to look through it, and they'll make a decision soon!I'll tell you their decision!",
        colour = discord.Colour.blue()))
    print(f"cyka here's the appeal: {ign}, {reason}, {length_of_p}, {punisher}, {reason_of_appeal}")

    tagged_creator = f"<@{creator.id}>"
    appeal_embed = discord.Embed(
        title = "New Appeal",
        description = f"{tagged_creator} has opened a new appeal.\nReact with ✅ to approve, or with ❌ to deny!",
        colour = discord.Colour.blue()
    )

    appeal_embed.add_field(name="IGN", value=ign)
    appeal_embed.add_field(name="Reason of punishment", value=reason)
    appeal_embed.add_field(name="Length of punishment", value=length_of_p)
    appeal_embed.add_field(name="Punisher", value=punisher)
    appeal_embed.add_field(name="Reason of appeal", value=reason_of_appeal)

    appeal_msg = await appeals_channel.send(embed=appeal_embed)
    await appeal_msg.add_reaction("✅")
    await appeal_msg.add_reaction("❌")

    data = str(appeal_msg.id) + "-"

    f = open("new_appeal_ids.txt", "a")
    f.write(data + "\n")
    f.close()   




async def create_ticket(type_, guild, creator):
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        guild.me: discord.PermissionOverwrite(read_messages=True),
        creator: discord.PermissionOverwrite(read_messages=True)
    }
    ticket_category = ""
    for category in guild.categories:
        if category.name == "Tickets":
            ticket_category = category
            break
        
    if ticket_category == "":
        ticket_category = await guild.create_category("Tickets")

    ticket_channel = await guild.create_text_channel(f'ticket-{creator.name}', overwrites=overwrites, category=ticket_category)

    embed_colour = ""
    if type_ == "Player Report":
        embed_colour = discord.Colour.orange()
    elif type_ == "Billing Support":
        embed_colour = discord.Colour.green()
    elif type_ == "Server Report":
        embed_colour = discord.Colour.red()
    elif type_ == "Staff Report":
        embed_colour = discord.Colour.blue()
    elif type_ == "Other":
        embed_colour = discord.Colour.purple()

    mention_user = f"<@{creator.id}>"
    embed = discord.Embed(
        title = "Welcome to your ticket!",
        description = f"{mention_user} needs help with **{type_}**\nPlease wait patiently for a staff member to assist you",
        colour = embed_colour
    )
    await ticket_channel.send(embed=embed)

    await post_commission(type_, guild, creator, ticket_channel.id)


async def post_commission(type_, guild, creator, id):
    commissions_channel = ""
    for channel in guild.channels:
        if channel.name == "new-support-tickets":
            commissions_channel = channel
            break

    embed_colour = ""
    if type_ == "Player Report":
        embed_colour = discord.Colour.orange()
    elif type_ == "Billing Support":
        embed_colour = discord.Colour.green()
    elif type_ == "Server Report":
        embed_colour = discord.Colour.red()
    elif type_ == "Staff Report":
        embed_colour = discord.Colour.blue()
    elif type_ == "Other":
        embed_colour = discord.Colour.purple()

    if commissions_channel == "":
        await creator.send(":x: **No commissions channel found.**\nPlease send this message to one of the staffs in the server!")
        return

    mention_user = f"<@{creator.id}>"
    embed = discord.Embed(
        title = "New Ticket",
        description = f"{mention_user} needs help with **{type_}**\nReact with :white_check_mark: to handle this ticket.",
        colour = embed_colour
    )

    msg = await commissions_channel.send(embed=embed)
    await msg.add_reaction("✅")

    data1 = str(msg.id) + ":" + str(id) + "-"

    f = open("new_ticket_ids.txt", "a")
    f.write(data1 + "\n")
    f.close()   

def Convert(string): 
    li = list(string.split("-")) 
    return li 


client.run(process.env.BOT_TOKEN)