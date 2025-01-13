import pandas as pd
from ydata_profiling import ProfileReport

df = pd.read_csv("s3/raw/real-or-fake-fake-jobposting-prediction.zip")

df = df.drop(columns=['fraudulent'])

df.to_csv("s3/bronze/real-or-fake-fake-jobposting-prediction.csv", index=False)

w_report = ProfileReport(df, title="Real or Fake Job Posting Dataset Report", explorative=True)
w_report.to_file("s3/bronze/real-or-fake-fake-jobposting-prediction.html")