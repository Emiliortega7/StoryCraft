import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import StoryCreator from "./StoryCreator";
import StoryViewer from "./StoryViewer";
import StoryList from "./StoryList";

function App() {
  return (
    <Router>
      <div>
        <Routes>
          <Route path="/" element={<StoryList />} />
          <Route path="/create" element={<StoryCreator />} />
          <Route path="/view/:id" element={<StoryViewer />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;