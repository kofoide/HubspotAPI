"""
Text
"""

import time
import pandas as pd
import requests
import globvars
import sqlalchemy
import pyodbc as odbc


# parse Single Event into dictionary from json received from Hubspot
def parse_single_event(eventrow):
    """
    Text
    """

    row = {}

    if 'recipient' in eventrow:
        row[u'recipient'] = eventrow['recipient']
    else:
        row[u'recipient'] = ''

    if 'created' in eventrow:
        row[u'created'] = eventrow['created']
    else:
        row[u'created'] = 0

    if 'emailCampaignId' in eventrow:
        row[u'emailCampaignId'] = eventrow['emailCampaignId']
    else:
        row[u'emailCampaignId'] = 0

    if 'deviceType' in eventrow:
        row[u'deviceType'] = eventrow['deviceType']
    else:
        row[u'deviceType'] = ''

    if 'type' in eventrow:
        row[u'type'] = eventrow['type']
    else:
        row[u'type'] = ''

    if 'appId' in eventrow:
        row[u'appId'] = eventrow['appId']
    else:
        row[u'appId'] = 0

    if 'location' in eventrow:
        if 'country' in eventrow['location']:
            row[u'country'] = eventrow['location']['country']
    else:
        row[u'country'] = ''

    if 'location' in eventrow:
        if 'state' in eventrow['location']:
            row[u'state'] = eventrow['location']['state']
    else:
        row[u'state'] = ''

    if 'location' in eventrow:
        if 'city' in eventrow['location']:
            row[u'city'] = eventrow['location']['city']
    else:
        row[u'city'] = ''

    if 'duration' in eventrow:
        row[u'duration'] = eventrow['duration']
    else:
        row[u'duration'] = 0

    if 'browser' in eventrow:
        if 'name' in eventrow['browser']:
            row[u'browser'] = eventrow['browser']['name']
    else:
        row[u'browser'] = ''

    return row


    # Get specific eventType for a sepcific campaign after defined time


def download_campaigneventtypesince(app, campaign, since, event, identity):
    """
    Text
    """
    meta_engine = sqlalchemy.create_engine(globvars.dsnalchemy)
    campeventurl = "/email/public/v1/events"
    appod = "&appId=" + str(app)
    campid = "&campaignId=" + str(campaign)
    timesince = "&startTimestamp=" + str(since)
    event = "&eventType=" + event

    url = globvars.baseurl + campeventurl + globvars.firstparm + appod + campid + timesince + event
    req = requests.get(url)

    callcount = 1
    result = req.json()['events']

    events = []
    for event in result:
        events = events + [parse_single_event(event)]

    # Put events in Database
    if events.count > 0:
        dataframe = pd.DataFrame.from_dict(events, orient='columns', dtype=None)
        dataframe['RunID'] = identity

        dataframe.to_sql(name="EmailEventTemp", con=meta_engine, schema="hs",
                         index=False, if_exists='append',
                         dtype=globvars.COLUMNSEMAILEVENTS)

    eventcount = len(events)

    # Subsequent calls to get rest of campaigns
    while req.json()['hasMore']:
        callcount = callcount + 1

        if (callcount % 10) == 0:
            time.sleep(1)

        offset = req.json()['offset']
        nexturl = url + "&offset=" + offset

        req = requests.get(nexturl)

        result = req.json()['events']

        events = []
        for event in result:
            events = events + [parse_single_event(event)]

        # Put events in Database
        if events.count > 0:
            dataframe = pd.DataFrame.from_dict(events, orient='columns', dtype=None)
            dataframe['RunID'] = identity

            dataframe.to_sql(
                name="EmailEventTemp", con=meta_engine,
                schema="hs", index=False, if_exists='append',
                dtype=globvars.COLUMNSEMAILEVENTS)

            eventcount = eventcount + len(events)

    return callcount, eventcount


def get_campaigneventtype(curs, meta_engine, eventtype, identity):
    """
    Text
    """

    # Get stats for this event
    sql = "SELECT * FROM hs.RunStatistics WHERE eventType = '%s'" % eventtype
    campaigns = pd.read_sql(sql, meta_engine)

    curs.execute("TRUNCATE TABLE hs.EmailEventTemp")

    # loop through the campaigns for this eventType
    for index, row in campaigns.iterrows():
        numcalls, eventcount = download_campaigneventtypesince(
            meta_engine, row['appId'], row['campaignId'],
            row['lastUpdatedTime'],
            row['eventType'], identity
        )

        output = "appId:%s\tcampaignId:%s\t%s:%s\texpected:%s\tcalls:%s" % (
            row['appId'], row['campaignId'], row['eventType'],
            eventcount, row['ExpectingAtLeast'], numcalls)

        print output

        #runningCallCount = runningCallCount + numCalls
        #totalEventCount = totalEventCount + eventCount

    curs.execute("EXEC hs.FinalizeEvent ?", eventtype)


def get_campaign_eventtypes(appid, campaignid, eventtype, identity):
    """
    TextDownl
    """
    conn = odbc.connect(globvars.dsnpyodbc, autocommit=True)
    curs = conn.cursor()

    curs.execute("TRUNCATE TABLE hs.EmailEventTemp")

    sql = """
    SELECT lastUpdatedTime, ExpectingAtLeast
    FROM hs.RunStatistics 
    WHERE appId = %s 
    AND campaignId = %s 
    AND eventType = '%s'""" % (appid, campaignid, eventtype)

    result = curs.execute(sql).fetchone()
    lastupdated = result[0]
    expecting = result[1]

    numcalls, eventcount = download_campaigneventtypesince(appid, campaignid, lastupdated, eventtype, identity)

    output = "appId:%s\tcampaignId:%s\t%s:%s\texpected:%s\tcalls:%s" % (
        appid, campaignid, eventtype, eventcount, expecting, numcalls)

    print output

        #runningCallCount = runningCallCount + numCalls
        #totalEventCount = totalEventCount + eventCount

    curs.execute("EXEC hs.Finalize")

def get_campaign_allevents(appid, campaignid, identity):
    """
    TextDownl
    """
    #loop through the event types
    conn = odbc.connect(globvars.dsnpyodbc, autocommit=True)
    curs = conn.cursor()
    sql = "SELECT * FROM hs.EventType"
    result = curs.execute(sql).fetchall()

    for row in result:
        get_campaign_eventtypes(appid, campaignid, row[0], identity)

def get_everything(identity):
    """
    TextDownl
    """
    #loop through the campaigns
    conn = odbc.connect(globvars.dsnpyodbc, autocommit=True)
    curs = conn.cursor()
    sql = "SELECT appId, campaignId FROM hs.CampaignStatistics"
    result = curs.execute(sql).fetchall()

    for row in result:
        get_campaign_allevents(row[0], row[1], identity)
        