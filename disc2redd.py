# bot.py

import os
import random
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='!d2r ',intents=intents)
bot.remove_command('help')

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='you, dm to contact staff!'))
    print(f'{bot.user.name} has connected to Discord!')
    
@bot.event
async def on_command_error(ctx, error):
    await ctx.send("Sorry, I do not recognize that command!")
    
@bot.event 
async def on_guild_join(guild):
    print(f"I have joined {guild}!")
    
@bot.event
async def ping(ctx):
    await ctx.send(f"pong! connection speed is {round(bot.latency * 1000)} ms")
    
@bot.command()
async def test(ctx):
    await ctx.send("hello")

@bot.command(name='help')
async def help(ctx):
    embed=discord.Embed(title="Help Commands", 
    description="""Hey! This is Discord2Reddit bot!
#This bot is currently in progress! More will be added soon.""", 
    color=0xfd5bfd)
    await ctx.send(embed=embed)

# image detection and upload
image_exts = ["png", "jpeg", "jpg", "jpg"]
# in the future provide support for mov, mp4, gif
@bot.event
async def on_message(message: discord.Message):
    if message.attachments:
       for attachment in message.attachments:
            if any(attachment.filename.lower().endswith(image) for image in image_exts):
                await attachment.save(f'{os.getcwd()}/attachments/{attachment.filename}')
                print(f"attachments saved")
    await bot.process_commands(message)
    
bot.run(TOKEN)