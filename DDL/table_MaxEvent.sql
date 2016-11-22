








IF OBJECT_ID(N'hs.MaxEvent', N'U') IS NOT NULL
  DROP TABLE hs.MaxEvent
GO


CREATE TABLE hs.MaxEvent(
	[appId] [bigint] NULL,
	[campaignId] [bigint] NULL,
	[eventType] [nvarchar](128) NULL,
	[lastUpdatedTime] [bigint] NULL,
	[lastUpdatedTimeSource] [varchar](6) NOT NULL,
	[countStats] [bigint] NULL,
	[countActual] [int] NULL,
	[lastUpdatedTimeStats] [bigint] NULL,
	[lastUpdatedTimeActual] [bigint] NULL
) ON [PRIMARY]
GO