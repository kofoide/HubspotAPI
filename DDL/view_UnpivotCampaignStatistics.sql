IF OBJECT_ID(N'hs.UnpivotCampaignStatistics', N'V') IS NOT NULL
  DROP VIEW hs.UnpivotCampaignStatistics
GO


CREATE VIEW hs.UnpivotCampaignStatistics
AS

SELECT
    appId
,   campaignId
,   lastUpdatedTime
,   eventType
,   [count]
FROM 
    (SELECT campaignId, appId, lastUpdatedTime, [open], click, spamreport, bounce, [deferred], delivered, dropped, forward, [print], processed, numQueued, numIncluded, [sent], statuschange
    FROM hs.CampaignStatistics) p
UNPIVOT
    ([count] FOR eventType IN 
        ([open], click, spamreport, bounce, [deferred], delivered, dropped, forward, [print], processed, numQueued, numIncluded, [sent], statuschange)
)AS unpvt
GO