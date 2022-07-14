import aiohttp
import xmltodict


async def get_feed_in_dict(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            xml = await response.text()
            return xmltodict.parse(xml)


def get_info_by_string_path(data: dict, path: str):
    split_path = path.split(".")
    for part in split_path:
        if not isinstance(data, dict):
            continue
        data = data[part]
    return data


async def get_feed_info(feed_data: dict):
    feed_url = feed_data["url"]
    feed_path = feed_data["data_path"]
    info_paths = feed_data["feed_paths"]
    recent_posts = await get_feed_in_dict(feed_url)
    last_post = get_info_by_string_path(recent_posts, feed_path)[0]
    post_info = {}
    for path in info_paths.keys():
        post_info[path] = get_info_by_string_path(last_post, info_paths[path])
    return post_info