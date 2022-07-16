"""
Commands for managing feeds
"""

from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
)

from GenericFeed.plugins.db import feed
from GenericFeed.plugins.utils.filters import is_sudoer


@Client.on_message(filters.command("add_feed") & is_sudoer)
async def add_feed(client: Client, message: Message):
    """
    Add a feed to the database.
    """
    args = message.text.split(" ")
    if len(args) < 3:
        await message.reply_text("Usage: /add_feed (feed url) (feed name)")
        return
    feed_url = args[1]
    feed_name = " ".join(args[2:])
    feed.add_feed(feed_url, feed_name)
    await message.reply_text("Feed added.")


@Client.on_message(filters.command("remfeed") & is_sudoer)
async def remove_feed(client: Client, message: Message):
    """
    Remove a feed from the database.
    """
    feed_list = feed.get_feeds()
    if len(feed_list) == 0:
        await message.reply_text("There is no feed to remove.")
        return

    buttons = [
        InlineKeyboardButton(
            feed_data["name"], callback_data=f"rem_feed|{str(feed_data['_id'])}"
        )
        for feed_data in feed_list
    ]
    markup = InlineKeyboardMarkup(buttons)
    await message.reply_text("Select a feed to remove:", reply_markup=markup)


@Client.on_callback_query(filters.regex("rem_feed"))
async def remove_feed(client: Client, callback_query: Message):
    """
    Remove a feed from the database.
    """
    feed_id = callback_query.data.split("|")[1]
    feed.remove_feed(feed_id)
    await callback_query.edit_text("Feed removed.")


@Client.on_message(filters.command("feeds"))
async def feeds(client: Client, message: Message):
    """
    Get all feeds from the database.
    """
    feed_list = list(feed.get_feeds())
    if len(feed_list) == 0:
        await message.reply_text("There is no feed.")
        return

    buttons = [
        InlineKeyboardButton(
            feed_data["name"], callback_data=f"path|{feed_data['_id']}"
        )
        for feed_data in feed_list
    ]
    await message.reply_text(
        "Select a feed:", reply_markup=InlineKeyboardMarkup([buttons])
    )


@Client.on_callback_query(filters.regex("path"))
async def path(client: Client, callback_query: CallbackQuery):
    """
    Get all paths from the feed and send in `InlineButtons`
    """
    feed_id = callback_query.data.split("|")[1]
    feed_data = feed.get_feed(feed_id)
    if feed_data is None:
        await callback_query.answer("The feed does not exist.", show_alert=True)
        return

    paths = feed_data["feed_paths"]

    buttons = []

    for path_name in paths.keys():
        buttons.append(
            [InlineKeyboardButton(path_name, callback_data=f"edit|{feed_id}|{path_name}")]
        )

    await callback_query.edit_message_text(
        "Select a path:", reply_markup=InlineKeyboardMarkup(buttons)
    )


@Client.on_callback_query(filters.regex("edit"))
async def edit_path(client: Client, callback_query: CallbackQuery):
    """
    Edit a path of a feed
    """
    feed_id = callback_query.data.split("|")[1]
    path_name = callback_query.data.split("|")[2]
    feed_data = feed.get_feed(feed_id)
    old_path = feed_data["feed_paths"][path_name]
    if feed_data is None:
        await callback_query.answer("The feed does not exist.", show_alert=True)
        return
    question = await callback_query.message.reply_text(
        f"Edit path {path_name}[`{old_path}`] of feed {feed_data['name']}:"
    )
    new_feed_path = await client.listen(
        callback_query.message.chat.id,
        filters.user(callback_query.from_user.id),
    )

    new_path = new_feed_path.text

    feed.change_feed_path(feed_id, path_name, new_path)

    await question.delete()
    await callback_query.edit_message_text(
        f"Path {path_name} changed from {old_path} to {new_path}"
    )