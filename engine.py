import os
from dotenv import load_dotenv
import psycopg2
import pysolr
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

dbname = os.getenv('DB_NAME')
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')
port = os.getenv('DB_PORT')

# Access the environment variables for Solr
solr_url = os.getenv('SOLR_URL')

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname=dbname,
    user=user,
    password=password,
    host=host,
    port=port
)


solr = pysolr.Solr(solr_url, timeout=10)

def serialize_row(row):
    data = {
        'id': row[0],
        'name': row[1],
        'address': row[2],
        "created_at": row[3],
        "latitude": row[4],
        "longitude": row[5]
    }
    for key in data:
        if isinstance(data[key], datetime):
            data[key] = data[key].strftime('%Y-%m-%dT%H:%M:%S')  # Adjust format as needed
    return data

try:

    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM public.events_fs_dates")
        rows = cursor.fetchall()

        if not rows:
            print("No data found in PostgreSQL.")
        else:
            # Index data into Solr
            solr.add([serialize_row(row) for row in rows])
            print(f"Indexed {len(rows)} documents into Solr.")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Close PostgreSQL connection
    conn.close()
