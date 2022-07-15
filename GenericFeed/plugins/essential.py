"""
Essentials commands for the bot.
"""
import time

from pyrogram import Client, filters
from pyrogram.types import Message

from GenericFeed.plugins.db import feed

from GenericFeed.plugins.utils.filters import is_sudoer


@Client.on_message(filters.command("ping"))
async def ping_command(client: Client, message: Message):
    """
    Calculate the ping of the bot.
    """
    start = time.time()
    ping_message = await message.reply_text("Pong!")
    end = time.time()
    ping = end - start
    await ping_message.edit_text(f"Ping: {ping * 1000}ms")


@Client.on_message(filters.command("start"))
async def start_command(client: Client, message: Message):
    """
    Command to verify if the bot is alive.
    """
    await message.reply_text("Hello!")