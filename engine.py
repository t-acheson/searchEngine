import datetime
import os
from dotenv import load_dotenv
import pysolr
import logging
import re

# Load environment variables from .env file
# load_dotenv()

# Access the environment variables for Solr
solr_url = "http://localhost:8983/solr/testcore"
# Initialize Solr client
solr = pysolr.Solr(solr_url, timeout=10)

def process_log_line(line):
    """
    Process a single line from the fake data text file and extract the necessary fields.
    Assumes the format is similar to:
    id, name, address, created_at, latitude, longitude
    """
    parts = line.strip().split('|')
    
    # Make sure the line has the expected number of parts
    if len(parts) != 6:
        print(f"Skipping invalid line: {line}")
        return None
    
    id, name, address, created_at, latitude, longitude = parts
    # Convert created_at to datetime format
    try:
        created_at = datetime.datetime.strptime(created_at, '%Y-%m-%dT%H:%M:%S')

    except ValueError:
        print(f"Skipping line with invalid date format: {line}")
        return None
    
    # Prepare the data for Solr
    data = {
        'id': id,
        'name': name,
        'address': address,
        'created_at': created_at.strftime('%Y-%m-%dT%H:%M:%S'),
        'latitude': latitude,
        'longitude': longitude
    }
    return data

# Function to process the entire file and index the data into Solr
def process_log_file(log_file='fakedata.txt'):
    with open(log_file, 'r') as file:
        # Read and process each line from the file
        for line in file:
            result = process_log_line(line)
            if result:
                try:
                    # Index the result into Solr
                    solr.add([result])
                    print(f"Indexed data for {result['name']} into Solr.")
                except Exception as e:
                    print(f"Error indexing data: {e}")

if __name__ == "__main__":
    # Process the log file and index results into Solr
    process_log_file('fake_data.txt')

# import os
# from dotenv import load_dotenv
# import psycopg2
# import pysolr
# from datetime import datetime

# # Load environment variables from .env file
# load_dotenv()

# dbname = os.getenv('DB_NAME')
# user = os.getenv('DB_USER')
# password = os.getenv('DB_PASSWORD')
# host = os.getenv('DB_HOST')
# port = os.getenv('DB_PORT')

# # Access the environment variables for Solr
# solr_url = os.getenv('SOLR_URL')


# # Connect to PostgreSQL
# conn = psycopg2.connect(
#     dbname=dbname,
#     user=user,
#     password=password,
#     host=host,
#     port=port
# )


# solr = pysolr.Solr(solr_url, timeout=10)

# def serialize_row(row):
#     data = {
#         'id': row[0],
#         'name': row[1],
#         'address': row[2],
#         "created_at": row[3],
#         "latitude": row[4],
#         "longitude": row[5]
#     }
#     for key in data:
#         if isinstance(data[key], datetime):
#             data[key] = data[key].strftime('%Y-%m-%dT%H:%M:%S')  # Adjust format as needed
#     return data

# try:

#     with conn.cursor() as cursor:
#         cursor.execute("SELECT * FROM public.events_fs_dates")
#         rows = cursor.fetchall()

#         if not rows:
#             print("No data found in PostgreSQL.")
#         else:
#             # Index data into Solr
#             solr.add([serialize_row(row) for row in rows])
#             print(f"Indexed {len(rows)} documents into Solr.")
# except Exception as e:
#     print(f"An error occurred: {e}")
# finally:
#     # Close PostgreSQL connection
#     conn.close()
