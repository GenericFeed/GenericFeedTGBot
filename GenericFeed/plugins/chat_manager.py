"""
Commands for the chat manager.
"""

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

from GenericFeed.plugins.db import chat


@Client.on_message(filters.command("add_chat"))
async def add_chat(client: Client, message: Message):
    """
    Add a chat to the database.
    """
    args = message.text.split(" ")
    if len(args) != 2:
        await message.reply_text("Usage: /add_chat <chat_id>")
        return
    chat_id = int(args[1])
    chat.add_chat(chat_id)


@Client.on_message(filters.command("remove_chat"))
async def remove_chat(client: Client, message: Message):
    """
    Remove a chat from the database.
    """
    chat_list = chat.get_chats()
    if len(chat_list) == 0:
        await message.reply_text("There is no chat to remove.")
        return

    chat_list = [chat_data['chat_id'] for chat_data in chat_list]
    buttons = [InlineKeyboardButton(chat_id, callback_data=f"rem_chat|{chat}") for chat_id in chat_list]
    markup = InlineKeyboardMarkup(buttons)
    await message.reply_text("Select a chat to remove:", reply_markup=markup)
    
@Client.on_callback_query(filters.regex("rem_chat"))
async def remove_chat(client: Client, callback_query: Message):
    """
    Remove a chat from the database.
    """
    chat_id = int(callback_query.data.split("|")[1])
    chat.remove_chat(chat_id)
    await callback_query.answer()
    await callback_query.edit_text("Chat removed.")


@Client.on_message(filters.command("chats"))
async def chats(client: Client, message: Message):
    """
    Get all chats from the database.
    """
    chat_list = chat.get_chats()
    if len(chat_list) == 0:
        await message.reply_text("There is no chat.")
        return

    chat_list = [f" - {chat_data['chat_id']}" for chat_data in chat_list]
    await message.reply_text("Chats:", "\n".join(chat_list))