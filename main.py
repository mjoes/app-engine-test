import time
from loguru import logger
from google.cloud import storage
import gspread
import google.auth

client = storage.Client()
bucket = client.bucket('auphonic-storage')
for blob in bucket.list_blobs(prefix='auphonic/'):
    if blob.name == 'auphonic/':
        pass
    else:
        print(blob.name)


SHEET_ID="1ZDPKh4zHLKUIqNo9XP9HMjxSd1TJwvTa_bjlEMY6m9M"
SHEET_NAME="meta"

import gspread

credentials, project_id = google.auth.default(
    scopes=[
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
)
print(credentials)
gc = gspread.authorize(credentials)
# gc = gspread.oauth()

spreadsheet = gc.open_by_key(SHEET_ID)
worksheet = spreadsheet.worksheet(SHEET_NAME)
rows = worksheet.get_all_records()

print(rows)
print("DONE NOW")

# def function_test():
#     i=0
#     k=0
#     while i < 10:
#         k=k+1
#         time.sleep(1)
#         logger.info(f"logging {k}")
#         print(f"test print no: {k}")

# function_test()