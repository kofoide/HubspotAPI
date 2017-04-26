"""
Text
"""

import time
import json
import requests
import functions


def parse_single_campaignstats(campaign):


    """
    Text
    """

    row = {}

    row[u'appId'] = campaign['appId']

    row[u'campaignId'] = campaign['id']

    # row[u'lastUpdatedTime'] = r['lastUpdatedTime']

    if 'name' in campaign:
        row[u'campaignName'] = campaign['name']
    else:
        row[u'campaignName'] = ''

    if 'appName' in campaign:
        row[u'appName'] = campaign['appName']
    else:
        row[u'appName'] = ''

    if 'numIncluded' in campaign:
        row[u'numIncluded'] = campaign['numIncluded']
    else:
        row[u'numIncluded'] = 0

    if 'numQueued' in campaign:
        row[u'numQueued'] = campaign['numQueued']
    else:
        row[u'numQueued'] = 0

    if 'processingState' in campaign:
        row[u'processingState'] = campaign['processingState']
    else:
        row[u'processingState'] = ''

    if 'subject' in campaign:
        row[u'subject'] = campaign['subject']
    else:
        row[u'subject'] = ''

    if 'type' in campaign:
        row[u'type'] = campaign['type']
    else:
        row[u'type'] = ''

    #counters
    camp = {}

    if 'counters' in campaign:
        camp = campaign['counters']

        if 'bounce' in camp:
            row[u'bounce'] = camp['bounce']
        else:
            row[u'bounce'] = 0

        if 'click' in camp:
            row[u'click'] = camp['click']
        else:
            row[u'click'] = 0

        if 'deferred' in camp:
            row[u'deferred'] = camp['deferred']
        else:
            row[u'deferred'] = 0

        if 'delivered' in camp:
            row[u'delivered'] = camp['delivered']
        else:
            row[u'delivered'] = 0

        if 'dropped' in campaign:
            row[u'dropped'] = campaign['dropped']
        else:
            row[u'dropped'] = 0

        if 'forward' in camp:
            row[u'forward'] = camp['forward']
        else:
            row[u'forward'] = 0

        if 'mta_dropped' in camp:
            row[u'mta_dropped'] = camp['mta_dropped']
        else:
            row[u'mta_dropped'] = 0

        if 'open' in camp:
            row[u'open'] = camp['open']
        else:
            row[u'open'] = 0

        if 'print' in campaign:
            row[u'print'] = campaign['print']
        else:
            row[u'print'] = 0

        if 'processed' in camp:
            row[u'processed'] = camp['processed']
        else:
            row[u'processed'] = 0

        if 'sent' in camp:
            row[u'sent'] = camp['sent']
        else:
            row[u'sent'] = 0

        if 'spamreport' in camp:
            row[u'spamreport'] = camp['spamreport']
        else:
            row[u'spamreport'] = 0

        if 'statuschange' in camp:
            row[u'statuschange'] = camp['statuschange']
        else:
            row[u'statuschange'] = 0

        if 'unsubscribed' in camp:
            row[u'unsubscribed'] = camp['unsubscribed']
        else:
            row[u'unsubscribed'] = 0

    return row


    # Get base campaigns

def get_single_campaignstats(baseurl, apikey, camp, noisy=False):
    """
    Text
    """

    campstaturl = "/email/public/v1/campaigns/" + str(camp['id'])
    appid = "&appId=" + str(camp['appId'])

    url = baseurl + campstaturl + apikey + appid

    req = requests.get(url)
    result = req.json()
    # js['lastUpdatedTime'] = camp['lastUpdatedTime']

    parsedcampaign = parse_single_campaignstats(result)
    if noisy:
        print "Getting Statistics for " + parsedcampaign['campaignName']

    return parsedcampaign

def get_all_campaignslist(baseurl, firstparm, noisy=False):
    """
    Text
    """

    campsurl = "/email/public/v1/campaigns/by-id"

    url = baseurl + campsurl + firstparm
    if noisy:
        print url
    req = requests.get(url)

    callcount = 1
    resultdict = req.json()['campaigns']

    with open('data.json', 'w') as outfile:
        if noisy:
            print 'dumping file'
        json.dump(req.json(), outfile)

    # Subsequent calls to get rest of campaigns
    while req.json()['hasMore']:
        if noisy:
            print 'Campaign List has more.'

        if (callcount % 10) == 0:
            time.sleep(1)

        offset = req.json()['offset']
        nexturl = url + "&offset=" + offset

        req = requests.get(nexturl)

        callcount = callcount + 1
        resultdict = resultdict + req.json()['campaigns']

    if noisy:
        print "Campaign List Call Count: " + str(callcount)

    return resultdict, callcount


def get_all_campaignsstats(baseurl, apikey, firstparm, noisy=False):
    """
    Text
    """

    camps = []

    campaigns, callcount = get_all_campaignslist(baseurl, firstparm, noisy)

    if noisy:
        print "Number of Campaigns: " + str(len(campaigns))

    for camp in campaigns:
        camps = camps + [get_single_campaignstats(baseurl, apikey, camp)]

    return callcount, camps
