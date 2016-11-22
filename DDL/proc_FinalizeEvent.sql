IF OBJECT_ID(N'hs.FinalizeEvent', N'P') IS NOT NULL
  DROP PROCEDURE hs.FinalizeEvent
GO


CREATE PROC [hs].[FinalizeEvent]
    @EventType VARCHAR(100)
AS

-- Remove the old MaxEvents for this EventType
DELETE FROM hs.MaxEvent WHERE eventType = @EventType;


WITH [stats] AS (
    SELECT
        appId
    ,   campaignId
    ,   lastUpdatedTime
    ,   eventType
    ,   [count]
    FROM 
       hs.UnpivotCampaignStatistics
    WHERE
        eventType = @EventType
)
, prev AS (
    SELECT
        appId
    ,   emailCampaignId AS campaignId
    ,   MAX(created) lastUpdatedTime
    ,   [type] AS eventType
    ,   COUNT(*) AS [count]
    FROM hs.EmailEventTemp
    GROUP BY emailCampaignId, [type], appId
)

INSERT INTO hs.MaxEvent(appId, campaignId, eventType, lastUpdatedTime, lastUpdatedTimeSource, countStats, CountActual, lastUpdatedTimeStats, lastUpdatedTimeActual)
SELECT
    ST.appId
,   ST.campaignId
,   ST.eventType
,   CASE
        WHEN ST.lastUpdatedTime > ISNULL(P.lastUpdatedTime, 0) THEN ST.lastUpdatedTime
        ELSE P.lastUpdatedTime
    END AS lastUpdatedTime
,   CASE
        WHEN ST.lastUpdatedTime > ISNULL(P.lastUpdatedTime, 0) THEN 'Stats'
        ELSE 'Actual'
    END AS lastUpdatedTimeSource
,   ST.[count] AS countStats
,   P.[count] AS countActual
,   ST.lastUpdatedTime As lastUpdatedTimeStats
,   P.lastUpdatedTime AS lastUpdatedTimeActual
FROM
            [stats] ST
FULL JOIN   prev    P   ON  ST.campaignId = P.campaignId
                        AND ST.appId = P.appId
                        AND ST.eventType = P.eventType


INSERT INTO hs.EmailEvent(RunID, appId, created, deviceType, emailCampaignId, recipient, [type], country, [state], city, duration, browser)
SELECT RunID, appId, created, deviceType, emailCampaignId, recipient, [type], country, [state], city, duration, browser FROM hs.EmailEventTemp

TRUNCATE TABLE hs.EmailEventTemp


GO


