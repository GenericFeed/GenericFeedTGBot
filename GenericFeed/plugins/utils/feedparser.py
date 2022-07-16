import feedparser
from typing import Dict, Any

NoneType = type(None)


def get_feed_as_dict(url: str) -> Dict:
    """
    It takes the last post in the feed and returns it as a dictionary.

    Example:
        feed_data = feedparser.parse("https://test.com/rss")
        print(type(feed_data))
        > `dict`
    """
    feed_data = feedparser.parse(url)
    return feed_data



def get_element_using_string(data: Dict,
                             string_path: str,
                             splitter: str = ".") -> Any:
    """
    Gets the last element that the string signals.

    Example:
        dict = {"data": {"sus": "pepsi man"}}
        path = "data/sus"
        final_value = get_element_using_string(dict, path)
        print(final_value)
        > `pepsi man`
    """
    if isinstance(string_path, NoneType):
        return string_path

    split_path = string_path.split(splitter)

    if not isinstance(split_path, list):
        split_path = [split_path]

    for part in split_path:
        if not isinstance(data, (dict, list)):
            continue
        if isinstance(data, dict):
            data = data[part]
        else:
            data = data[0][part]
        
    return data

def get_last_post(feed_data: dict):
    feed_url = feed_data["url"]
    feed_path = feed_data["data_path"]
    info_paths = feed_data["feed_paths"]
    recent_posts = get_feed_as_dict(feed_url)
    last_post = get_element_using_string(recent_posts, feed_path)
    post_info = {}
    for path in info_paths.keys():
        post_info[path] = get_element_using_string(last_post, info_paths[path])
    return post_info