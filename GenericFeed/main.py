"""
GenericFeed main class
"""

# TODO: Make function to send the news with formatting.
import asyncio
from pyrogram import Client
from GenericFeed import config

from GenericFeed.plugins.db import feed, chat
from GenericFeed.plugins.utils import feedparser

async def loopFeed(client: Client) -> None:
    """
    Loop to get the news from the feeds.
    """
    while True:
        feed_list = feed.get_feeds()
        for feed_data in feed_list:
            feed_url = feed_data['url']
            feed_name = feed_data['name']
            feed_data_path = feed_data['data_path']
            feed_paths = feed_data['feed_paths']
            last_guid = feed_data['last_guid']
            feed_data = feedparser.get_feed_in_dict(feed_url)
            last_post = feedparser.get_info_by_string_path(feed_data, feed_data_path)[0]
            post_info = {}
            for path in feed_paths.keys():
                post_info[path] = feedparser.get_info_by_string_path(last_post, feed_paths[path])
            if last_guid == post_info['guid']:
                continue
            chat_list = chat.get_chats()
            for chat_data in chat_list:
                chat_id = chat_data['chat_id']
                await client.send_message(chat_id, config.NEWS_FORMAT.format(**post_info))
            feed.change_last_guid(feed_url, post_info['guid'])
        await asyncio.sleep(config.LOOP_TIME)

            

class GenericFeedBot(Client):
    def __init__(self):
        super().__init__(
            name="bot",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            plugins={'root': 'GenericFeed.plugins'}
        )
