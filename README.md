# GenericFeed
GenericFeed is a news aggregator made for Telegram;

> Project still under development, feel free to contribute to it.

### Configuration:

```py
"""
GenericFeed/config.py
"""

# Get the API_ID and the API_HASH from my.telegram.org;
API_ID: int = None or os.getenv('API_ID')
API_HASH: str = None or os.getenv('API_HASH')

# Get BOT_TOKEN from https://t.me/BotFather;
BOT_TOKEN: str = None or os.getenv('BOT_TOKEN')

# Get MONGODB_URL from https://www.mongodb.com/atlas;
MONGODB_URL: str = None or os.getenv('MONGODB_URL')
```

### Requirements:

- MongoDB
- Python3
- Telegram API Secrets
- Bot Token
