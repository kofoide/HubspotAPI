IF OBJECT_ID(N'hs.DownloadRun', N'U') IS NOT NULL
  DROP TABLE hs.DownloadRun
GO



CREATE TABLE hs.DownloadRun(
	[RunID] [int] IDENTITY(1,1) NOT NULL,
	[RunDate] [datetime] NOT NULL
) ON [PRIMARY]
GO