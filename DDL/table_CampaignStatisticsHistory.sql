IF OBJECT_ID(N'hs.CampaignStatisticsHistory', N'U') IS NOT NULL
  DROP TABLE hs.CampaignStatisticsHistory
GO



CREATE TABLE hs.CampaignStatisticsHistory(
	[RunID] [int] NOT NULL,
	[appId] [int] NULL,
	[appName] [varchar](255) NULL,
	[bounce] [int] NULL,
	[campaignId] [int] NULL,
	[campaignName] [varchar](255) NULL,
	[click] [int] NULL,
	[deferred] [int] NULL,
	[delivered] [int] NULL,
	[dropped] [int] NULL,
	[forward] [int] NULL,
	[lastUpdatedTime] [bigint] NULL,
	[mta_dropped] [int] NULL,
	[numIncluded] [int] NULL,
	[numQueued] [int] NULL,
	[open] [int] NULL,
	[print] [int] NULL,
	[processed] [int] NULL,
	[processingState] [varchar](255) NULL,
	[sent] [int] NULL,
	[spamreport] [int] NULL,
	[statuschange] [int] NULL,
	[subject] [varchar](255) NULL,
	[type] [varchar](255) NULL,
	[unsubscribed] [int] NULL
) ON [PRIMARY]
GO