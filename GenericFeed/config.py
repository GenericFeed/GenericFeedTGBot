"""
Config file
"""
import os
from dotenv import load_dotenv

load_dotenv(".env")

# Get the API_ID and the API_HASH from my.telegram.org;
API_ID: int = None or os.getenv('API_ID')
API_HASH: str = None or os.getenv('API_HASH')

# Get BOT_TOKEN from https://t.me/BotFather;
BOT_TOKEN: str = None or os.getenv('BOT_TOKEN')

# Get MONGODB_URL from https://www.mongodb.com/atlas;
MONGODB_URL: str = None or os.getenv('MONGODB_URL')

NEWS_FORMAT = """
Name: {title}
URL: {link} | Published: {pubDate}
Description: {description}
ID: {guid}
"""

LOOP_TIME = 10 # in seconds