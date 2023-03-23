import time
from loguru import logger
from google.cloud import storage
import gspread
import requests
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import duckdb

# gc = gspread.service_account(filename=filepath_json)
gc = gspread.oauth()

SOURCE_BUCKET = "auphonic-storage"
DESTINATION_BUCKET = "archive-verslibre"
SHEET_ID="1ZDPKh4zHLKUIqNo9XP9HMjxSd1TJwvTa_bjlEMY6m9M"
SHEET_NAME="meta"

client = storage.Client()
source_bucket = client.bucket(SOURCE_BUCKET)
destination_bucket = client.bucket(DESTINATION_BUCKET)
filepath_json = 'home/dev1/sheetsapi.json'

spreadsheet = gc.open_by_key(SHEET_ID)
worksheet = spreadsheet.worksheet(SHEET_NAME)
rows = worksheet.get_all_records()

df = pd.DataFrame.from_dict(rows)
df = df[["tag", "show_nr"]]

con = duckdb.connect('show_nrs.db')
con.sql("CREATE TABLE IF NOT EXISTS shownrs AS SELECT * FROM df")
x=con.sql("SELECT * from shownrs").df()
print(x)
