import requests
import time
import logging

# Configure logging
logging.basicConfig(filename='search_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

def count_entries_with_word(word):
    solr_url = 'http://localhost:8983/solr/testcore/select'
    params = {
        'q': f'name:{word}',
        'rows': 0,
        'wt': 'json'
    }

    # Measure the time taken to perform the search
    start_time = time.time()
    response = requests.get(solr_url, params=params)
    end_time = time.time()

    # Calculate the elapsed time
    elapsed_time = end_time - start_time

    data = response.json()
    num_found = data['response']['numFound']

    # Log the search word, number of entries found, and the time taken
    logging.info(f"Search word: {word}, Number of entries: {num_found}, Time taken: {elapsed_time:.4f} seconds")

    return num_found, elapsed_time

words = "Summer", "Park", "Beach", "Sun", "Avenue", "1", "2"
for word in words:
    count, search_time = count_entries_with_word(word)
    print(f"Number of entries with the word '{word}': {count}")
    print(f"Time taken for the search: {search_time:.4f} seconds")
    print()
