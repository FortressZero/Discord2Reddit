# bot.py

import os
import logging
import random
import socket
import sys

import asyncpraw

reddit = asyncpraw.Reddit(
    client_id=os.getenv('CLIENT_ID'),
    client_secret=os.getenv('CLIENT_SECRET'),
    password=os.getenv('REDDIT_PASSWORD'),
    user_agent=os.getenv('USER_AGENT'),
    username=os.getenv('REDDIT_USERNAME'),
)

# reminder to self: look at using HTTPS proxy with asyncpraw, logging, etc.