"""
Text1
"""

import time


# parse the Epoch into a real date
def parsedate(datenum):
    """
    Text
    """

    return time.localtime(round(int(datenum/1000)))


def stringifydate(thisdate):
    """
    Text
    """

    return time.strftime("%a, %d %b %Y %H:%M:%S", thisdate)


# parse Single Campaign Statistics from the json received from Hubspot
