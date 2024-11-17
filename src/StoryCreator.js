import React, { useState, useCallback } from 'react';

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.log(error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return <h1>Something went wrong.</h1>;
    }

    return this.props.children; 
  }
}

const InteractiveStoryEditor = () => {
  const [story, setStory] = useState({
    title: '',
    content: '',
    choices: [{ id: 1, text: '', nextPart: '' }],
  });

  const handleChange = useCallback((e) => {
    const { name, value } = e.target;
    try {
      setStory({ ...story, [name]: value });
    } catch (error) {
      console.error("Failed to update story:", error);
    }
  }, [story]);

  const handleChoiceChange = useCallback((index, e) => {
    const { name, value } = e.target;
    try {
      const choices = [...story.choices];
      choices[index] = { ...choices[index], [name]: value };
      setStory({ ...story, choices });
    } catch (error) {
      console.error(`Failed to update choice ${index}:`, error);
    }
  }, [story]);

  const addChoice = useCallback(() => {
    try {
      const newChoice = { id: story.choices.length + 1, text: '', nextPart: '' };
      setStory({ ...story, choices: [...story.choices, newChoice] });
    } catch (error) {
      console.error("Failed to add a new choice:", error);
    }
  }, [story]);

  const removeChoice = useCallback((index) => {
    try {
      const choices = story.choices.filter((_, i) => i !== index);
      setStory({ ...story, choices });
    } catch (error) {
      console.error(`Failed to remove choice ${index}:`, error);
    }
  }, [story]);

  return (
    <ErrorBoundary>
      <div>
        <h2>Create/Edit Your Interactive Story</h2>
        <form>
          <div>
            <label>Title:</label>
            <input
              type="text"
              name="title"
              value={story.title}
              onChange={handleChange}
            />
          </div>
          <div>
            <label>Story Content:</label>
            <textarea
              name="content"
              value={story.content}
              onChange={handleChange}
            />
          </div>
          {story.choices.map((choice, index) => (
            <div key={choice.id}>
              <label>Choice {index + 1}:</label>
              <input
                type="text"
                name="text"
                value={choice.text}
                onChange={(e) => handleChoiceChange(index, e)}
              />
              <input
                type="text"
                name="nextPart"
                value={choice.nextPart}
                onChange={(e) => handleChoiceChange(index, e)}
              />
              <button type="button" onClick={() => removeChoice(index)}>Remove</button>
            </div>
          ))}
          <button type="button" onClick={addChoice}>Add Choice</button>
        </form>
      </div>
    </ErrorBoundary>
  );
};

export default InteractiveStoryEditor;