import datetime
import discord
from discord.ext import commands
from discord import DMChannel
from discord.utils import get
import asyncio
intents = discord.Intents.default()
intents.members = True  #must have presence and members intent enabled in dev portal

client = commands.Bot(command_prefix = '!', intents=intents, help_command=None) #prefix etc.

@client.event
async def on_ready():
    print("Bot is ready.")
    await client.change_presence(status=discord.Status.online, activity=discord.Game('ModMail | DM me for help!')) #change status to whatever you like.


@client.listen()
async def on_message(message):
    member = message.author
    if member.id == client.user.id:
        return 
    
    guild = client.get_guild(id=) #guild_Id
    category = discord.utils.get(guild.categories, id=) #category id where you want to set up modmail.
    overwrites = {
    guild.default_role: discord.PermissionOverwrite(read_messages=False),
    guild.me: discord.PermissionOverwrite(read_messages=True)
}
    if isinstance(message.channel, DMChannel): 
        if member != client.user: 
            channel = discord.utils.get(guild.channels, name=f"{member.id}") 
            if channel is None: 
                await category.create_text_channel(name=f"{member.id}", overwrites=overwrites)
                oof = discord.Embed(
                    title = "Ticket Created!",
                    description = "\nPlease send your message again!",
                    colour = discord.Colour(0x0de404)
                )
                oof.timestamp = datetime.datetime.utcnow()
                await member.send(embed=oof)     
            elif channel is not None:
                for i in message.attachments:
                    embed = discord.Embed(
                        title = "Message Sent",
                        colour = discord.Colour(0x0de404)
                    )
                    embed.set_image(url=f"{i.url}")  
                    embed.timestamp = datetime.datetime.utcnow()
                    await member.send(embed=embed)
                    embed = discord.Embed(
                        title = 'Message Recieved',
                        colour = discord.Colour.blurple()
                    )
                    embed.set_author(name=f"{member}", icon_url=member.avatar_url)
                    embed.set_image(url=f"{i.url}")
                    embed.timestamp = datetime.datetime.utcnow()
                    await message.channel.send(embed=embed)
                    return     
                embed = discord.Embed(
                    title = "Message Sent",
                    description = f"{message.content}",
                    colour = discord.Colour(0x0de404)
                )  
                embed.timestamp = datetime.datetime.utcnow()
                await member.send(embed=embed)
                embed = discord.Embed(
                    title = 'Message Recived',
                    description = f'\n{message.content}',
                    colour = discord.Colour(0xbf309d)
                )
                embed.timestamp = datetime.datetime.utcnow()
                embed.set_author(name=f"{member}", icon_url=member.avatar_url)                       
                await channel.send(embed=embed)
        

    if message.channel.category == category: 
        TheID = message.channel.name 
        ID = int(TheID)
        reporter = guild.get_member(ID) 
        if reporter is None: 
            print("Member not found.")   
        elif reporter is not None:
            for i in message.attachments:
                embed = discord.Embed(
                    title = "Message Sent",
                    colour = discord.Colour(0x0de404)
                )
                embed.set_image(url=f"{i.url}")  
                embed.timestamp = datetime.datetime.utcnow()
                await channel.send(embed=embed)
                embed = discord.Embed(
                    title = 'Message Recieved',
                    colour = discord.Colour.blurple()
                )
                embed.set_author(name=f"{member}", icon_url=member.avatar_url)
                embed.set_image(url=f"{i.url}")
                embed.timestamp = datetime.datetime.utcnow()
                await member.send(embed=embed)
                return    
            await message.delete(delay=None)
            embed = discord.Embed(
                title = "Message Sent",
                description = f"{message.content}",
                colour = discord.Colour(0x0de404)
            )  
            embed.timestamp = datetime.datetime.utcnow()
            await message.channel.send(embed=embed)
            embed = discord.Embed(
                title = 'Message Recieved',
                description = f'\n{message.content}',
                colour = discord.Colour.blurple()
            )
            embed.set_author(name=f"{member}", icon_url=member.avatar_url)
            embed.timestamp = datetime.datetime.utcnow()
            await reporter.send(embed=embed)    


@client.command()
@commands.has_permissions(manage_channels=True)
async def close(ctx, *, reason=None):
    guild = ctx.guild
    reporter = guild.get_member(int(ctx.channel.name))
    channel = discord.utils.get(guild.channels, name=f"{reporter.id}")
    if reason is None:
        await channel.delete(reason=reason)
        embed = discord.Embed(
            title = 'Ticket Closed',
            description = 'Your Ticket has been closed by the Staff Team.\n',
            colour = discord.Colour(0xFF0055)
        )
        embed.add_field(name="Reason", value="No reason provided.")
        embed.timestamp = datetime.datetime.utcnow()
        await reporter.send(embed=embed)
    else:
        await channel.delete(reason=reason)
        embed = discord.Embed(
            title = 'Ticket Closed',
            description = 'Your Ticket has been closed by the Staff Team.\n',
            colour = discord.Colour(0xFF0055)
        )
        embed.add_field(name="Reason", value=f"{reason}")
        embed.timestamp = datetime.datetime.utcnow()
        await reporter.send(embed=embed)    

client.run('') #token of your bot
