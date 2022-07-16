"""
Config file
"""
import os
from typing import Union
from dotenv import load_dotenv

load_dotenv(".env")

# Get the API_ID and the API_HASH from my.telegram.org;
API_ID: int = None or os.getenv('API_ID')
API_HASH: str = None or os.getenv('API_HASH')

# Get BOT_TOKEN from https://t.me/BotFather;
BOT_TOKEN: str = None or os.getenv('BOT_TOKEN')

# Get MONGODB_URL from https://www.mongodb.com/atlas;
MONGODB_URL: str = None or os.getenv('MONGODB_URL')

NEWS_FORMAT: str = """
Name: [{title}]({link})
{splitter}
Description: {summary}.

Published: {pubDate}
"""

SUDOERS: list = [
    2138770172,
]

LOOP_TIME: Union[int, float] = 10 # in seconds