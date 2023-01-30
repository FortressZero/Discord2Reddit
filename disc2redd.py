# bot.py

import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from nudenet import NudeClassifier

classifier = NudeClassifier()

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
subreddit = os.getenv('SUBREDDIT')

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='!d2r ',intents=intents)
bot.remove_command('help')
bot.post_id = 0

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
    await ctx.send(subreddit)

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
        nsfwFlag = False
        curr = 0
        parent_path = f'{os.getcwd()}/attachments/{bot.post_id}'
        os.mkdir(parent_path)
        for attachment in message.attachments:
            if any(attachment.filename.lower().endswith(image) for image in image_exts):
                path_name = f'{parent_path}/{attachment.filename}'
                curr += 1
                await attachment.save(path_name)
                print(f"attachment saved")
                classifier_result = classifier.classify(path_name)
                if (classifier_result[path_name]['unsafe'] > .85):
                    os.remove(path_name)
                    break
                elif (classifier_result[path_name]['unsafe'] > .6):
                    nsfwFlag = True
        if not os.listdir(parent_path):
            os.rmdir(parent_path)
            print(f"not a valid image format")
        bot.post_id = bot.post_id + 1
        bot.post_id = bot.post_id % 100000
        title = ""
        if message.content:
            title = message.content
        else:
            title = "testing"
        # change above so that title is "submitted by USER"
        # and any message content is a reply to the post
        # submit_images(title, nsfwFlag, count, subreddit)
    await bot.process_commands(message)

bot.run(TOKEN)