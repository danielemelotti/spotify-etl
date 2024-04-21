import json
import sqlite3
import sqlalchemy
import pandas as pd
from sqlalchemy.orm import sessionmaker
import requests
from datetime import datetime, timedelta


# Validation function: checking for undesirable scenarios
def check_if_valid_data(df: pd.DataFrame) -> bool:
    # Check if df is empty (meaning no song played in the last 24hrs)
    if df.empty:
        print("No songs downloaded. Finishing execution.")
        return False
    
    # Primary Key Check (check for duplicates)
    if pd.Series(df["played_at"]).is_unique:
        pass
    else:
        raise Exception("Primary Key Check is violated.")
    
    # Check for nulls
    if df.isnull().values.any():
        raise Exception("Null values found.")
    
    # # Check that all timestamps are from the last 24hrs
    # yesterday = datetime.now() - timedelta(days = 1)
    # yesterday = yesterday.replace(hour = 0, minute = 0, second = 0, microsecond = 0)

    # timestamps = df["timestamp"].tolist()
    # for timestamp in timestamps:
    #     if datetime.strptime(timestamp, "%Y-%m-%d") != yesterday:
    #         raise Exception("At least one of the returned songs does not come from within the last 24 hrs.")

    # return True


def run_spotify_etl():
    
    DATABASE_LOCATION = "sqlite:///my_played_tracks.sqlite"
    USER_ID = "YOUR USER ID" #SENSITIVE
    TOKEN = "YOUR ACCESS TOKEN" #SENSITIVE

    # EXTRACT
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer {token}".format(token = TOKEN)
    }

    # We run the feed daily - every day we want to see what songs we played in the last 24hrs
    today = datetime.now()
    yesterday = today - timedelta(days = 1)
    yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000

    r = requests.get("https://api.spotify.com/v1/me/player/recently-played?after={time}".format(time = yesterday_unix_timestamp), headers = headers)

    data = r.json()

    # Have a look at what you listened to in the last 24hrs
    # print(data)

    song_names = []
    artist_names = []
    played_at_list = []
    timestamps = []

    # Loop through the songs, extract the elements of interest
    for song in data["items"]:
        song_names.append(song["track"]["name"])
        artist_names.append(song["track"]["album"]["artists"][0]["name"])
        played_at_list.append(song["played_at"])
        timestamps.append(song["played_at"][0:10])

    # Create a dictionary, then a pandas df
    song_dict = {
        "song_name": song_names,
        "artist_name": artist_names,
        "played_at": played_at_list,
        "timestamp": timestamps
    }

    song_df = pd.DataFrame(song_dict, columns = ["song_name", "artist_name", "played_at", "timestamp"])

    # You can have a look at the df
    # print(song_df)

    # TRANSFORM (Validate)
    if check_if_valid_data(song_df):
        print("Valid data, proceed to Load")

    # LOAD

    # Create an engine
    engine = sqlalchemy.create_engine(DATABASE_LOCATION)
    conn = sqlite3.connect("my_played_tracks.sqlite")
    cursor = conn.cursor() #database pointer

    sql_query = """
    CREATE TABLE IF NOT EXISTS my_played_tracks(
        song_name VARCHAR(200),
        artist_name VARCHAR(200),
        played_at VARCHAR(200),
        timestamp VARCHAR(200),
        CONSTRAINT primary_key_constraint PRIMARY KEY (played_at)
    )
    """

    cursor.execute(sql_query)
    print("Opened database successfully.")

    # Loading the dataframe data to the SQL database
    try:
        song_df.to_sql("my_played_tracks", engine, index = False, if_exists = "append")
    except:
        print("Data already exists in the database.")

    conn.close()
    print("Close database successfully.")