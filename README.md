# HubspotAPI

## Download Email Events from Hubspot API

This app will download all email events from Hubspot API. It uses Campaign Statistics to decide what timeframe to begin downloading from.

Resources:
* MSSQL - Run DDL in the project against your database
* Schema named "hs" in database
* ODBC named "Prod" to connect to database
* Windows environment variable named HubSpotAPIKey with your API key value
* Windows environment variable named HubSpotAPIDatabase with the name of the database

Put the event types you want to download in the hs.DownloadableEventType table
