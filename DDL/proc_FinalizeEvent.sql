-- EXEC hs.FinalizeEvent 'click'

IF OBJECT_ID(N'hs.FinalizeEvent', N'P') IS NOT NULL
  DROP PROCEDURE hs.FinalizeEvent
GO


CREATE PROC [hs].[FinalizeEvent]
    @EventType VARCHAR(100)
AS

-- Remove the old MaxEvents for this EventType
DELETE FROM hs.MaxEvent WHERE eventType = @EventType;

INSERT INTO hs.MaxEvent(appId, campaignId, eventType, lastUpdatedTime, CountActual)
SELECT
    appId
,   emailCampaignId AS campaignId
,   [type] AS eventType
,   MAX(created) + 1 lastUpdatedTime
,   COUNT(DISTINCT recipient) AS [count]
FROM hs.EmailEventTemp
WHERE [type] = @EventType
GROUP BY
	emailCampaignId
,	[type]
,	appId


INSERT INTO hs.EmailEvent(RunID, appId, created, deviceType, emailCampaignId, recipient, [type], country, [state], city, duration, browser)
SELECT RunID, appId, created, deviceType, emailCampaignId, recipient, [type], country, [state], city, duration, browser
FROM hs.EmailEventTemp

TRUNCATE TABLE hs.EmailEventTemp
GO