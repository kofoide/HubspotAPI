IF OBJECT_ID(N'hs.RunStatistics', N'V') IS NOT NULL
  DROP VIEW hs.RunStatistics
GO


CREATE VIEW hs.RunStatistics
AS

SELECT
    N.appId
,   N.campaignId
,   N.eventType
,   ISNULL(O.lastUpdatedTime, 0) AS lastUpdatedTime
,   N.[count] - ISNULL(O.countStats, 0) AS ExpectingAtLeast
FROM
            hs.UnpivotCampaignStatistics    N
LEFT JOIN   hs.MaxEvent                     O   ON  N.campaignId = O.campaignId
                                                AND N.appId = O.appId
                                                AND N.eventType = O.eventType
WHERE
    N.lastUpdatedTime > ISNULL(O.lastUpdatedTime, 0)
AND N.[count] > 0
GO