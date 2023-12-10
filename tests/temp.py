from datetime import datetime, timezone
import pandas as pd


date_string = '2014-01-01'
date_object = datetime.strptime(date_string, '%Y-%m-%d').replace(tzinfo=timezone.utc)
timestamp_seconds = date_object.timestamp()
timestamp_milliseconds = timestamp_seconds * 1000
print(int(timestamp_milliseconds))

date = timestamp_milliseconds / 1000
datetime_object = pd.to_datetime(date, unit='s')
print(datetime_object)
