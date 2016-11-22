IF OBJECT_ID(N'hs.DownloadableEventType', N'U') IS NOT NULL
  DROP TABLE hs.DownloadableEventType
GO



CREATE TABLE hs.DownloadableEventType(
	[eventType] [varchar](50) NULL
) ON [PRIMARY]
GO