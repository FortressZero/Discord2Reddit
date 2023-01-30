# bot.py

import os
import shutil

import asyncpraw
from asyncpraw.models import Subreddit

reddit = asyncpraw.Reddit(
    client_id=os.getenv('CLIENT_ID'),
    client_secret=os.getenv('CLIENT_SECRET'),
    password=os.getenv('REDDIT_PASSWORD'),
    user_agent=os.getenv('USER_AGENT'),
    username=os.getenv('REDDIT_USERNAME'),
    ratelimit_seconds = 300, #rmv later
)

async def submit_images(msg_title: str, subreddit: Subreddit, nsfwFlag: bool, post_id: int) -> None:
    #subreddit = reddit.subreddit(os.getenv('SUBREDDIT'))
    parent_path = f'{os.getcwd()}/attachments/{post_id}'
    if not os.path.exists(parent_path):
        print(f"directory not found!")
        return
    reddit_files = os.listdir(parent_path)
    if not reddit_files:
        return
    elif len(reddit_files) == 1:
        await subreddit.submit_image(title=msg_title, image_path=reddit_files[0], nsfw=nsfwFlag)
    else:
        images = [{"image_path": f"{parent_path}/{filename}"} for filename in reddit_files]
        # might not work? check back here l8r
        await subreddit.submit_gallery(title=msg_title,  nsfw=nsfwFlag)
    shutil.rmtree(parent_path)

# reminder to self: look at using HTTPS proxy with asyncpraw, logging, etc.