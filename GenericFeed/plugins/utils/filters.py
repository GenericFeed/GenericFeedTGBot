"""
GenericFeed custom filters
"""
from pyrogram.types import Message
from GenericFeed.config import SUDOERS

def is_sudoer(_, message: Message) -> bool:
    """
    Check if the user is a sudoer.
    """
    return message.from_user.id in SUDOERS