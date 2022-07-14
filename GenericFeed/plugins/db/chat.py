"""
Chat Manager in the database
"""

from GenericFeed import database

def check_chat(chat_id: int) -> bool:
    """
    Check if a chat is in the database.
    """
    return database.chats.find_one({"chat_id": chat_id}) is not None

def add_chat(chat_id: int) -> None:
    """
    Add a chat to the database.
    """
    database.chats.insert_one({"chat_id": chat_id})


def remove_chat(chat_id: int) -> None:
    """
    Remove a chat from the database.
    """
    database.chats.delete_one({"chat_id": chat_id})


def get_chats() -> list:
    """
    Get all chats from the database.
    """
    return database.chats.find({}, {"_id": 0})


def get_chat(chat_id: int) -> dict:
    """
    Get a chat from the database.
    """
    return database.chats.find_one({"chat_id": chat_id}, {"_id": 0})
