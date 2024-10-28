import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import StoryCreator from "./StoryCreator";
import StoryViewer from "./StoryViewer";
import StoryList from "./StoryList";
import StorySearch from "./StorySearch"; // Assuming you will create this component

function App() {
  return (
    <Router>
      <div>
        <nav style={{ marginBottom: "20px" }}>
          <Link to="/" style={{ marginRight: "10px" }}>Home</Link>
          <Link to="/create" style={{ marginRight: "10px" }}>Create Story</Link>
          <Link to="/search">Search Stories</Link>
        </nav>
        <Routes>
          <Route path="/" element={<StoryList />} />
          <Route path="/create" element={<StoryCreator />} />
          <Route path="/view/:id" element={<StoryViewer />} />
          <Route path="/search" element={<StorySearch />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
```
```javascript
// StorySearch.js
import React, { useState } from 'react';

function StorySearch() {
    const [query, setQuery] = useState('');
    const [results, setResults] = useState([]);

    const handleChange = (event) => {
        setQuery(event.target.value);
    };

    const handleSearch = async () => {
        // Assuming your stories are fetched from an API or similar
        // This is a placeholder for your actual search logic
        // You will need to implement actual search logic based on how your stories are stored
        setResults([{id: '1', title: 'Example Story Title', content: 'Content of the story based on search query'}]);
    };

    return (
        <div>
            <h2>Search Stories</h2>
            <input
                type="text"
                value={query}
                onChange={handleChange}
                placeholder="Search by title or content"
            />
            <button onClick={handleSearch}>Search</button>
            <ul>
                {results.map((story) => (
                    <li key={story.id}>{story.title} - {story.content}</li>
                ))}
            </ul>
        </div>
    );
}

export default StorySearch;