import os
import pinboard
import yaml
import time
import Levenshtein
from collections import defaultdict
from albertv0 import *

# see https://albertlauncher.github.io/docs/extensions/python/

__iid__ = "PythonInterface/v0.1"
__prettyname__ = "Pinboard"
__version__ = "0.0.1"
__trigger__ = "pb"
__author__ = "Alexandre Leblanc"

HOME_DIR = os.environ["HOME"]
APITOKEN = os.environ["PINBOARD_API"]
PINBOARD_DIR = os.environ.get("PINBOARD_DIR", os.path.join(HOME_DIR, ".config/pinboard"))
PINBOARD_DB = os.path.join(PINBOARD_DIR, "pinboard_db")
TIME_KEY = "epoch"


def bookmark_dict(bookmark, db):
    for tag in bookmark.tags:
        db[tag].append([bookmark.description, bookmark.url])


def refresh(pb):
    bookmark_list = pb.posts.all()
    dict_db = defaultdict(list)
    for bm in bookmark_list:
        bookmark_dict(bm, dict_db)
    dict_db[TIME_KEY] = time.time()
    with open(PINBOARD_DB, "r+") as pb:
        pb.write(yaml.dump(dict_db))


# The api allow us to fetch once every 5 minutes max
def need_refresh(epoch):
    return time.time() - epoch > (60 * 6)


def read_yaml():
    with open(PINBOARD_DB, "r+") as pbrc:
        db = yaml.load(pbrc.read())
        return db


def heuristic(key, string):
    return Levenshtein.ratio(key, string) > 0.5


def match_key(string, dict_db):
    l = defaultdict(list)
    for k, v in dict_db.items():
        if heuristic(k, string):
            l[k] = v
    return l


def run(string):
    pb = pinboard.Pinboard(APITOKEN)
    yaml_db = read_yaml()
    if yaml_db is None or need_refresh(yaml_db.get(TIME_KEY, 0)):
        refresh(pb)
        yaml_db = read_yaml()
    return match_key(string, yaml_db)


def handleQuery(query):
    if query.isTriggered:
        return agregate(query)


def agregate(query):
    results = run(query.string)
    items = []
    for k, v in results.items():
        for l in v:
            items.append(
                Item(
                    id=__prettyname__,
                    text="{0} {1}".format(k, l[0]),
                    actions=[
                        UrlAction("Open", l[1])
                    ]
                )
            )
    return items


if __name__ == "__main__":
    x = run("linux")
    print(x)
