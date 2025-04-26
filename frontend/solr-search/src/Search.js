import React, { useState } from 'react';

const Search = () => {
    const [query, setQuery] = useState('');
    const [results, setResults] = useState([]);
    const [error, setError] = useState(null);

    const handleSearch = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch(`/solr/testcore/select?q=name:${encodeURIComponent('*' + query + '*')} OR address:${encodeURIComponent('*' + query + '*')}&wt=json`);

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            setResults(data.response.docs);
        } catch (error) {
            setError(error.toString());
        }
    };
    return (
        <div>
            <form onSubmit={handleSearch}>
                <input 
                    type="text" 
                    value={query} 
                    onChange={(e) => setQuery(e.target.value)} 
                    placeholder="Search..." 
                />
                <button type="submit">Search</button>
            </form>
            {error && <div>Error: {error}</div>}
            <ul>
                {results.map(result => (
                    <li key={result.id}>
                        {result.name}
                        {result.address}
                        {result.created_at}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default Search;
