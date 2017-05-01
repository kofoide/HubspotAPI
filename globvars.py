"""
Global Variables
"""

import configparser
import sqlalchemy


parser = configparser.ConfigParser()

#if os.name == "posix":
#    parser.read(u'../config.ini')
#else:
#    parser.read(u"..\config.ini")

parser.read(u'../config.ini')

key = parser.get('Hubspot', 'APIKEY')
apikey = "?hapikey=" + key
limit = "&limit=1000"
firstparm = apikey + limit
baseurl = "https://api.hubapi.com"
runningcallcount = 0
dsnalchemy = parser.get('Database', 'HubspotSqlAlc')
dsnpyodbc = parser.get('Database', 'HubspotPy')

COLUMNSCAMPAIGNSTATISTICS = {
    'appId': sqlalchemy.types.INTEGER(),
    'appName': sqlalchemy.types.VARCHAR(length=255),
    'bounce': sqlalchemy.types.INTEGER(),
    'campaignId': sqlalchemy.types.INTEGER(),
    'campaignName': sqlalchemy.types.VARCHAR(length=255),
    'click': sqlalchemy.types.INTEGER(),
    'deferred': sqlalchemy.types.INTEGER(),
    'delivered': sqlalchemy.types.INTEGER(),
    'dropped': sqlalchemy.types.INTEGER(),
    'forward': sqlalchemy.types.INTEGER(),
    #    , 'lastUpdatedTime': sqlalchemy.types.BIGINT(),
    'mta_dropped': sqlalchemy.types.INTEGER(),
    'numIncluded': sqlalchemy.types.INTEGER(),
    'numQueued': sqlalchemy.types.INTEGER(),
    'open': sqlalchemy.types.INTEGER(),
    'print': sqlalchemy.types.INTEGER(),
    'processed': sqlalchemy.types.INTEGER(),
    'processingState': sqlalchemy.types.VARCHAR(length=255),
    'sent': sqlalchemy.types.INTEGER(),
    'spamreport': sqlalchemy.types.INTEGER(),
    'statuschange': sqlalchemy.types.INTEGER(),
    'subject': sqlalchemy.types.VARCHAR(length=255),
    'type': sqlalchemy.types.VARCHAR(length=255),
    'unsubscribed': sqlalchemy.types.INTEGER()
}

COLUMNSCAMPAIGNSTATISTICSHISTORY = {
    'RunID': sqlalchemy.types.INTEGER(),
    'appId': sqlalchemy.types.INTEGER(),
    'appName': sqlalchemy.types.VARCHAR(length=255),
    'bounce': sqlalchemy.types.INTEGER(),
    'campaignId': sqlalchemy.types.INTEGER(),
    'campaignName': sqlalchemy.types.VARCHAR(length=255),
    'click': sqlalchemy.types.INTEGER(),
    'deferred': sqlalchemy.types.INTEGER(),
    'delivered': sqlalchemy.types.INTEGER(),
    'dropped': sqlalchemy.types.INTEGER(),
    'forward': sqlalchemy.types.INTEGER(),
    #    , 'lastUpdatedTime': sqlalchemy.types.BIGINT(),
    'mta_dropped': sqlalchemy.types.INTEGER(),
    'numIncluded': sqlalchemy.types.INTEGER(),
    'numQueued': sqlalchemy.types.INTEGER(),
    'open': sqlalchemy.types.INTEGER(),
    'print': sqlalchemy.types.INTEGER(),
    'processed': sqlalchemy.types.INTEGER(),
    'processingState': sqlalchemy.types.VARCHAR(length=255),
    'sent': sqlalchemy.types.INTEGER(),
    'spamreport': sqlalchemy.types.INTEGER(),
    'statuschange': sqlalchemy.types.INTEGER(),
    'subject': sqlalchemy.types.VARCHAR(length=255),
    'type': sqlalchemy.types.VARCHAR(length=255),
    'unsubscribed': sqlalchemy.types.INTEGER()
}

COLUMNSEMAILEVENTS = {
    'RunID': sqlalchemy.types.INTEGER(),
    'appId': sqlalchemy.types.INTEGER(),
    'created': sqlalchemy.types.BIGINT(),
    'deviceType': sqlalchemy.types.VARCHAR(length=255),
    'emailCampaignId': sqlalchemy.types.INTEGER(),
    'recipient': sqlalchemy.types.VARCHAR(length=255),
    'type': sqlalchemy.types.VARCHAR(length=255),
    'country': sqlalchemy.types.VARCHAR(length=255),
    'state': sqlalchemy.types.VARCHAR(length=255),
    'city': sqlalchemy.types.VARCHAR(length=255),
    'duration': sqlalchemy.types.INTEGER(),
    'browser': sqlalchemy.types.VARCHAR(length=255)
}

