import time
from loguru import logger
from google.cloud import storage
import gspread
import google.auth
import os

client = storage.Client()
bucket = client.bucket('auphonic-storage')
for blob in bucket.list_blobs(prefix='auphonic/'):
    if blob.name == 'auphonic/':
        pass
    else:
        print(blob.name)

## part 2

SHEET_ID="1ZDPKh4zHLKUIqNo9XP9HMjxSd1TJwvTa_bjlEMY6m9M"
SHEET_NAME="meta"
filepath = 'home/dev1/sheetsapi.json'
# scopes=[
#     'https://www.googleapis.com/auth/spreadsheets',
#     'https://www.googleapis.com/auth/drive'
# ]

gc = gspread.service_account(filename=filepath)
# gc = gspread.oauth()

spreadsheet = gc.open_by_key(SHEET_ID)
worksheet = spreadsheet.worksheet(SHEET_NAME)
rows = worksheet.get_all_records()

print(rows)
print("DONE NOW")

