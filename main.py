from telethon.sync import TelegramClient

import pandas as pd
import datetime
import re

import matplotlib.pyplot as plt

api_id = "your id here"
api_hash = "your api hash here"

group = 'your telegram group here'

df = pd.DataFrame(columns=["text", "date"])

timeframe = datetime.datetime(2024, 1, 1)

with TelegramClient('test', api_id, api_hash) as client:
    for message in client.iter_messages(group, offset_date=timeframe, reverse=True):
        data = {"text": message.text, "date": message.date}
        df = df._append(data, ignore_index=True)

# Define a regex pattern to match "M", "U", or "S" (case-insensitive) followed by a number
pattern = r'(?i)(M|U|S)(\d+)'

# Extract matching patterns from the text column using str.extract()
df['line'] = df['text'].str.extract(pattern).apply(lambda x: ''.join(x.dropna()), axis=1).str.upper()

df = df.replace('', pd.NA)
df = df.dropna(subset=['line'])

df['hour'] = df['date'].dt.hour
df['day'] = df['date'].dt.strftime('%A') #dt.dayofweek
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year

plt.hist(df['hour'], bins=range(min(df['hour']), max(df['hour']) + 1, 1), edgecolor='black')


plt.xlabel('Hour')
plt.ylabel('Frequency')
plt.title('Histogram of Hour')


plt.show()