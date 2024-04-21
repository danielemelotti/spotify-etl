# Building a Data Pipeline for Spotify data

The aim of this project is to build a data pipeline (data feed), covering the ETL process. We use the Spotify API to download the data related to which songs were most listened to on an individual account, then save that data to a database. The data feed runs daily via Apache Airflow.

# Extract
We download the data under the form of a JSON file using the Spotify API. We are interested in downloading the songs we listened to the day before, on a daily basis. 
To do so, we need to create an account on Spotify for Developers, and we need to generate an authentication code, which we then exchange for an access token. See `auth.py` and `spotify_token.py`.

# Transform (Validation Step)
We conduct simple checks, such as that the data is not containing missing values and that there are no duplicates.

# Load
We load our data on SQLite database.

# Scheduling
We use Apache Airflow for task scheduling.