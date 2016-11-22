IF OBJECT_ID(N'hs.EmailEventTemp', N'U') IS NOT NULL
  DROP TABLE hs.EmailEventTemp
GO


CREATE TABLE hs.EmailEventTemp(
	[RunID] [int] NULL,
	[appId] [int] NULL,
	[created] [bigint] NULL,
	[deviceType] [varchar](255) NULL,
	[emailCampaignId] [int] NULL,
	[recipient] [varchar](255) NULL,
	[type] [varchar](50) NULL,
	[country] [varchar](255) NULL,
	[state] [varchar](255) NULL,
	[city] [varchar](255) NULL,
	[duration] [int] NULL,
	[browser] [varchar](255) NULL
) ON [PRIMARY]
GO