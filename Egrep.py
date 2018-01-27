from albertv0 import *
import subprocess
import os

# see https://albertlauncher.github.io/docs/extensions/python/

__iid__ = "PythonInterface/v0.1"
__prettyname__ = "Egrep"
__version__ = "0.0.1"
__trigger__ = "egn"
__author__ = "Alexandre Leblanc"

HOME_DIR = os.environ["HOME"]
NOTES_DIR = os.environ.get("NOTES_DIR", os.path.join(HOME_DIR, "notes"))


def handleQuery(query):
    if query.isTriggered:
        return agregate(query)


def run(query):
    process = subprocess.Popen(["egrep", "-r", query, NOTES_DIR], stdout=subprocess.PIPE)
    comm_tuples = process.communicate()
    return comm_tuples[0].splitlines()


def agregate(query):
    results = run(query.string)
    items = []
    for line in results:
        r = line[-(len(line) - len(NOTES_DIR) - 1):]
        items.append(
            Item(
                id=__prettyname__,
                text="egrep {0}".format(r),
                actions=[
                    ClipAction("Copied to buffer", r)
                ]
            )
        )
    return items
