# bot.py

import os
import shutil

import asyncpraw
from asyncpraw.models import Subreddit
from dotenv import load_dotenv

load_dotenv()

async def submit_images(msg_title: str, subreddit: str, nsfwFlag: bool, post_id: int) -> None:
    parent_path = f'{os.getcwd()}/attachments/{post_id}'
    if not os.path.exists(parent_path):
        print(f"directory not found!")
        return
    reddit = asyncpraw.Reddit(
        client_id=os.getenv('CLIENT_ID'),
        client_secret=os.getenv('CLIENT_SECRET'),
        password=os.getenv('REDDIT_PASSWORD'),
        user_agent=os.getenv('USER_AGENT'),
        username=os.getenv('REDDIT_USERNAME'),
        ratelimit_seconds = 60, #rmv later
    )
    subreddit = await reddit.subreddit(subreddit)
    reddit_files = os.listdir(parent_path)
    if not reddit_files:
        print(f"no files detected")
        return
    elif len(reddit_files) == 1:
        await subreddit.submit_image(title=msg_title, image_path=f"{parent_path}/{reddit_files[0]}", nsfw=nsfwFlag)
        print(f"submit single image complete")
    else:
        images = [{"image_path": f"{parent_path}/{filename}"} for filename in reddit_files]
        # might not work? check back here l8r
        await subreddit.submit_gallery(title=msg_title, images=images, nsfw=nsfwFlag)
        print(f"submit gallery complete")
    shutil.rmtree(parent_path)
    await reddit.close()
# reminder to self: look at using HTTPS proxy with asyncpraw, logging, etc.