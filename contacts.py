"""
Text
"""

import requests

# Get Contact Statistics
# Return: Dictionary
def get_contact_stats(baseurl, apikey):
    """
    Text
    """

    staturl = "/contacts/v1/contacts/statistics"
    url = baseurl + staturl + apikey
    req = requests.get(url)

    return req.json()
