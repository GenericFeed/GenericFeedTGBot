"""
Feed Manager in the database
"""
from bson.objectid import ObjectId

from GenericFeed import database
from GenericFeed.plugins.utils.exceptions import FeedAlreadyExists

DEFAULT_FEED_INFO = {
    "name": None,
    "url": None,
    "data_path": "rss.channel.item",
    "feed_paths": {
        "title": "title.#text",
        "link": "link.@href",
        "description": "description.#text",
        "guid": "id",
        "pubDate": "pubDate",
        "thumbnail": None,
    },
    "last_guid": None
}


def check_feed(feed_url: str) -> bool:
    """
    Check if a feed exists in the database.
    """
    return database.feeds.find_one({"url": feed_url}) is not None


def add_feed(feed_url: str, feed_name: str) -> None:
    """
    Add a feed to the database.
    """
    if check_feed(feed_url):
        raise FeedAlreadyExists
        
    feed_data = DEFAULT_FEED_INFO.copy()
    feed_data['name'] = feed_name
    feed_data['url'] = feed_url
    database.feeds.insert_one(feed_data)


def remove_feed(ObjectID: str) -> None:
    """
    Remove a feed from the database.
    """
    database.feeds.delete_one({"_id": ObjectId(ObjectID)})


def get_feeds() -> list:
    """
    Get all feeds from the database.
    """
    return database.feeds.find({})


def get_feed(feed_url: str) -> dict:
    """
    Get a feed from the database.
    """
    return database.feeds.find_one({"_id": ObjectId(feed_url)})

def change_last_guid(feed_url: str, guid: str) -> None:
    """
    Change the last update of a feed.
    """
    database.feeds.update_one({"url": feed_url}, {"$set": {"last_guid": guid}})


def change_feed_path(feed_id, path_name: str, value: str) -> None:
    """
    Change a feed path.
    """
    paths = get_feed(feed_id)["feed_paths"]
    paths[path_name] = value
    
    database.feeds.update_one({"_id": ObjectId(feed_id)}, {"$set": {"feed_paths":paths}})