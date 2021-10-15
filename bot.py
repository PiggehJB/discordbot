import discord
from discord.colour import Color
from discord.ext import commands, tasks
from colorama import Fore
from discord.ext.commands import has_permissions, MissingPermissions
from datetime import datetime
import os
from keep_alive import keep_alive

# Gets token from replit's secrets, if you're just using a .env file do token = os.getenv('token') instead (or simply put your token in the token variable)
token = os.environ['token']

# Defines my prefix
prefix = "-"

# Enabling all intents, must also enable on your bot dev page!!
intents = discord.Intents.all()

bot = commands.Bot(command_prefix=prefix, intents=intents)

# When bot is loaded
@bot.event
async def on_ready():
    print(f"{Fore.GREEN}The bot is online!{Fore.RESET}")
    # Start my loop
    pipreminder.start()

@bot.command()
@has_permissions(kick_members=True)
async def kick(ctx, kick_member:discord.Member,*, reason=None):
    # If the user tries to kick the bot (wont happen anyway but want to tell them off)
    if kick_member == bot.user:
        await ctx.send("You can't kick me :angry:")
    # Making sure the user's role is higher than the person they're tryna kick
    elif kick_member.top_role >= ctx.author.top_role:
        await ctx.send("This person's role is higher or equal to yours!")
    # Kicks the member
    else:
        await kick_member.kick(reason=reason)
        
# Error checking
@kick.error
async def kick_error(message, error):
    # If no perms
    if isinstance(error, MissingPermissions):
        await message.send("You don't have permissions to kick this member")

@bot.event
async def on_message(ctx):
    if ctx.author == bot.user:
        pass
    else:
        full = ctx.content
        # If someone says pip, this is for all the ppls who ask about pip not working
        if "pip" in full:
            await ctx.channel.send("If you're having any issues with pip, check out <#895483227244994641>")
        else:
            pass
        # Prevents server invites
        if ".gg" in full:
            await ctx.delete()
            await ctx.channel.send("Server invites aren't allowed here! {}".format(ctx.author.mention))
    await bot.process_commands(ctx)

counter = 0
@tasks.loop(hours=3)
async def pipreminder():
    global counter
    channel = bot.get_channel(894746091382272000)
    # Getting the previous 2 messages (probably don't need to search 2 messages but whatever)
    messages = await channel.history(limit=2).flatten()
    
    # Adds +1 for each msg that is sent by the bot
    for msg in messages:
        if msg.author == bot.user:
            counter +=1
    # If it's 1 (or more), I won't send another message to prevent duplicates from being sent
    if counter >= 1:
        print(f"{Fore.RED}Duplicate detected, ignoring new message request\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Fore.RESET}")
        counter = 0
    else:
        await channel.send("If you're having any issues with pip, check out <#895483227244994641>\n`Automated Message`")
        print(f"{Fore.GREEN}Sent pip reminder to {Fore.MAGENTA}{channel}\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Fore.RESET}")

# If member joins
@bot.event
async def on_member_join(member):
    wlc_channel = bot.get_channel(898420446125490186)
    embed = discord.Embed(title=f"Welcome {member.name}!", color = discord.colour.Color.from_rgb(255,192,203)).set_author(name=f"{member.guild}", icon_url=f"{member.guild.icon_url}")
    embed.add_field(name="Thank you for joining the server!", value=f"If you have any questions please check out <#895483227244994641> before asking in any support channels, also, please read\
    your code before asking, it saves ours and your time. If you're having an error with any code from a video, please ask in <#894746091382272000> -- Thank you :)", inline=True)
    embed.set_footer(icon_url=f"{member.guild.icon_url}", text=f"The server now has {member.guild.member_count} members!\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    await wlc_channel.send(embed=embed)
    msg = await wlc_channel.send(f"{member.mention}")
    await msg.delete()

# If member is removeed or leaves
@bot.event
async def on_member_remove(member):
    wlc_channel = bot.get_channel(898420446125490186)
    embed = discord.Embed(title=f"{member.name} Left", color=Color.red()).set_author(name=f"{member.guild}", icon_url=f"{member.guild.icon_url}")
    embed.add_field(name=f"Goodbye {member.name}", value="Goodbye! Sorry to see you go :sob:")
    embed.set_footer(icon_url=f"{member.guild.icon_url}", text=f"The server now has {member.guild.member_count} members!\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    await wlc_channel.send(embed=embed)

# Keep my bot being hosted 24/78 (flask + uptime robot)
keep_alive()
bot.run(token)
