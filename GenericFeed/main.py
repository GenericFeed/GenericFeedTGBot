"""
GenericFeed main class
"""

# TODO: Make function to send the news with formatting.
import asyncio
import logging
from posixpath import split
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
            last_guid = feed_data['last_guid']
            post_info = feedparser.get_last_post(feed_data)
            if last_guid == post_info['guid']:
                continue
            message_text = config.NEWS_FORMAT.format(
                    title=post_info['title'],
                    splitter = "—",
                    link=post_info['link'],
                    pubDate=post_info['pubDate'],
                    summary=post_info['summary'][:200] + '..' if len(post_info['summary']) > 4000 else post_info['summary'],
                    guid=post_info['guid'],
                )
            chat_list = chat.get_chats()
            for chat_data in chat_list:
                chat_id = chat_data['chat_id']
                if feed_data['feed_paths']['thumbnail'] is not None:
                    print(post_info['thumbnail'])
                    try:
                        await client.send_photo(
                            chat_id,
                            post_info['thumbnail'],
                            caption=message_text
                        )
                    except Exception as e:
                        logging.error(f"{e}")
                        continue
                else:
                    await client.send_message(chat_id, message_text)
            feed.change_last_guid(feed_url, post_info['guid'])
        await asyncio.sleep(config.LOOP_TIME)

            

class GenericFeedBot(Client):
    def __init__(self):
        super().__init__(
            name="bot",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            plugins={'root': 'GenericFeed.plugins'},
            in_memory=True
        )

    async def start(self):
        await super().start()
        while True:    
            # try:
            await loopFeed(self)
            # except Exception as e:
            #     await asyncio.sleep(config.LOOP_TIME)
                