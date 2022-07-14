"""
GenericFeed execution file
"""

import logging

from GenericFeed.main import GenericFeedBot
from GenericFeed import database


# Custom logging format
logging.basicConfig(
    level=logging.INFO,
    format="%(name)s.%(funcName)s | %(levelname)s | %(message)s",
    datefmt="[%X]",
)


# To avoid some pyrogram annoying log
logging.getLogger("pyrogram.syncer").setLevel(logging.WARNING)
logging.getLogger("pyrogram.client").setLevel(logging.WARNING)


if __name__ == "__main__":
    logging.info("GenericFeed is on.")
    try:
        GenericFeedBot().run()
    except KeyboardInterrupt:
        logging.info("GenericFeed was turned off by the user.")
