# searchEngine
solr start      
solr create_core -c testcore
python fakedate.py
python engine.py
npm start 


Basic search engine that uses Apache Solr for indexing and querying data, with a React frontend to display search results. The data is fetched from a PostgreSQL database and indexed into Solr.

Returns all entries of street addresses in New York City based on key word search. Suggested search terms: "Summer", "1", "Taco".
