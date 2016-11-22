IF OBJECT_ID(N'hs.EmailEvent', N'U') IS NOT NULL
  DROP TABLE hs.EmailEvent
GO



CREATE TABLE hs.EmailEvent(
	[RunID] [int] NULL,
	[appId] [int] NULL,
	[created] [bigint] NULL,
	[deviceType] [varchar](255) NULL,
	[emailCampaignId] [int] NULL,
	[recipient] [varchar](255) NULL,
	[type] [varchar](50) NULL,
	[InsertDateTime] [datetime] NULL CONSTRAINT [DF__EmailEven__Inser__48756F2C]  DEFAULT (getdate()),
	[country] [varchar](255) NULL,
	[state] [varchar](255) NULL,
	[city] [varchar](255) NULL,
	[duration] [int] NULL,
	[browser] [varchar](255) NULL
) ON [PRIMARY]
GO