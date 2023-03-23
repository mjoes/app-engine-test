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
con = duckdb.connect('show_nrs.db')

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

file_list = source_bucket.list_blobs(prefix='auphonic/')

def get_publish(date_rec):
    exp_date = date_rec + timedelta(days=1)
    if exp_date < datetime.today():
        publish_date=(datetime.today()+timedelta(days=1)).strftime("%Y-%m-%dT10:00:00Z")
    else:
        publish_date=exp_date.strftime("%Y-%m-%dT10:00:00Z")
    return publish_date

def get_name(df_active, tag):
    show_name = df_active['show_name'].iloc[0]
    show_nr = con.sql(f"SELECT show_nr from shownrs where tag = '{tag}'").df().iloc[0]
    dj_name = df_active['dj_name'].iloc[0]

    if dj_name is not None:
        name=f"{show_name} #{int(show_nr)} - w/ {dj_name}"
    else:
        name=f"{show_name} #{int(show_nr)}"
    return name

def move_blob(source_bucket, file_name, destination_bucket, date, show_name):
    """Moves a blob from one bucket to another with a new name."""
    destination_generation_match_precondition = 0
    
    month = date.month
    year = date.year

    source_blob_name = f"{source_bucket}/{file_name}"
    source_blob = source_bucket.blob(source_blob_name)
    destination_blob_name = f"{destination_bucket}/radio_shows/{year}/{month}/{show_name}/{file_name}"

    blob_copy = source_bucket.copy_blob(
        source_blob, destination_bucket, destination_blob_name, if_generation_match=destination_generation_match_precondition,
    )
    source_bucket.delete_blob(source_blob_name)
    return blob_copy

for blob in file_list:
    if blob.name == 'auphonic/':
        pass
    else:
        file_name = blob.name
        tag = file_name.split('-',2)[1]
        df_active=df[df["tag"]==tag]
        picpath=df_active["picture"].iloc[0]
        show_name=df_active["show_name"].iloc[0]

        date_rec = datetime.strptime(file_name.split(' ',2)[0], '%Y%m%d')
        publish_date = get_publish(date_rec)
        name = get_name(df_active, tag)

        data=df_active[['description','tags-0-tag','tags-1-tag','tags-2-tag','tags-3-tag','tags-4-tag']].dropna(axis=1, how='all').to_dict('records')
        payload=data[0]
        payload.update({'name':f"{name}",'publish_date':f'{publish_date}','disable_comments':True,'hide_stats':True})
        
        mp3 = source_bucket.blob(f"{SOURCE_BUCKET}/{file_name}")
        picture = source_bucket.blob(f"{SOURCE_BUCKET}/pictures/{picpath}")

        try:
            file = {
                "mp3":open(mp3,'rb'),
                "picture":open(picture,'rb')
            }
            url = "https://api.mixcloud.com/upload/?access_token="
            response = requests.request("POST", url,data=payload,files=file)
            print(response.text)
            if 'RateLimitException' in response.text:
                logger.error("Failed: Rate limit exception")
                break
            elif 'Success' in response.text:
                logger.info(f"Upload passed for: {file_name}")
                con.sql(f"UPDATE shownrs SET show_nr = show_nr + 1 where tag = '{tag}'")
                move_blob(source_bucket, mp3, destination_bucket, date_rec, show_name)

        except:
            logger.error("Upload failed, check logs")
            pass

con.close()
