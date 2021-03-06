-- EXEC hs.FinalizeEvent 'click'

IF OBJECT_ID(N'hs.Finalize', N'P') IS NOT NULL
  DROP PROCEDURE hs.Finalize
GO

CREATE PROC hs.Finalize
AS

IF OBJECT_ID('tempdb..#tmp') IS NOT NULL DROP TABLE #tmp
-- Rollup campaign events
SELECT
	COUNT(DISTINCT recipient) AS RecordCount
,	MAX(created) AS MaxDate
,	appId
,	emailCampaignId
,	[type]
INTO #tmp
FROM hs.EmailEventTemp
GROUP BY
	appId
,	emailCampaignId
,	[type]


-- Remove the old MaxEvents for this new download
DELETE ME
FROM
			hs.MaxEvent	ME
 WHERE
	EXISTS (SELECT 1 FROM #tmp T WHERE ME.appId = T.appId AND ME.campaignId = T.emailCampaignId AND ME.eventType = T.[type])


-- Add the new MaxEvents for this download
INSERT INTO hs.MaxEvent(appId, campaignId, eventType, lastUpdatedTime, CountActual)
SELECT
    appId
,   emailCampaignId AS campaignId
,   [type] AS eventType
,   MaxDate + 1 lastUpdatedTime
,   RecordCount AS [count]
FROM #tmp


-- Store these new events
INSERT INTO hs.EmailEvent(RunID, appId, created, deviceType, emailCampaignId, recipient, [type], country, [state], city, duration, browser)
SELECT RunID, appId, created, deviceType, emailCampaignId, recipient, [type], country, [state], city, duration, browser
FROM hs.EmailEventTemp


TRUNCATE TABLE hs.EmailEventTemp
