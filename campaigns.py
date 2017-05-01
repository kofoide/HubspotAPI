"""
Text
"""

import time
import json
import requests
import globvars
import pandas as pd
import sqlalchemy


def parse_single_campaign(campaign):
    """
    Receives the json from the Campaign Statistics API call result

    Returns parsed dictionary of campaign statistics
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

def download_single_campaignstats(camp, noisy=False):
    """
    Makes call to Campaign Statistics API for a specific campaign

    Returns dictionary of the campaign statistics
    """
    # API endpoint
    campstaturl = "/email/public/v1/campaigns/" + str(camp['id'])
    appid = "&appId=" + str(camp['appId'])
    # API URL
    url = globvars.baseurl + campstaturl + globvars.apikey + appid
    # Go Get em...
    req = requests.get(url)
    campaign = req.json()

    parsedcampaign = parse_single_campaign(campaign)
    if noisy:
        print "Getting Statistics for " + parsedcampaign['campaignName']

    return parsedcampaign

def download_campaign_list(noisy=False):
    """
    Gets a list of campaigns
    """
    # API endpoint
    campsurl = "/email/public/v1/campaigns/by-id"
    # API URL
    url = globvars.baseurl + campsurl + globvars.firstparm

    callcount = 1
    req = requests.get(url)
    campaigndict = req.json()['campaigns']

    if noisy:
        with open('data.json', 'w') as outfile:
            print url
            json.dump(req.json(), outfile)

    # Are there more to get?
    while req.json()['hasMore']:
        if noisy:
            print 'There are more to get...'

        # Slow down trigger...
        if (callcount % 10) == 0:
            time.sleep(1)

        #Get the offset parameter
        offset = req.json()['offset']
        # API URL
        nexturl = url + "&offset=" + offset
        # Go get em...
        callcount = callcount + 1
        req = requests.get(nexturl)
        campaigndict = campaigndict + req.json()['campaigns']

    if noisy:
        print "Campaign List Call Count: " + str(callcount)

    return campaigndict, callcount


def get_all_campaignstats(noisy=False):
    """
    Text
    """

    camps = []
    # First get the list of campaigns
    campaigns, callcount = download_campaign_list(noisy)

    if noisy:
        print "Number of Campaigns: " + str(len(campaigns))

    # Get the stats about each campaign
    for camp in campaigns:
        camps = camps + [download_single_campaignstats(camp)]

    # put them in database
    meta_engine = sqlalchemy.create_engine(globvars.dsnalchemy)
    pd.DataFrame.from_dict(camps, orient='columns', dtype=None).to_sql(name="CampaignStatistics", schema="hs", con=meta_engine, index=False, if_exists="replace", dtype=globvars.COLUMNSCAMPAIGNSTATISTICS)

    return callcount
