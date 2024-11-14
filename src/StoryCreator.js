import React, { useState } from 'react';

const InteractiveStoryEditor = () => {
  const [story, setStory] = useState({
    title: '',
    content: '',
    choices: [{ id: 1, text: '', nextPart: '' }]
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setStory({ ...story, [name]: value });
  };

  const handleChoiceChange = (index, e) => {
    const { name, value } = e.target;
    const choices = [...story.choices];
    choices[index] = { ...choices[index], [name]: value };
    setStory({ ...story, choices });
  };

  const addChoice = () => {
    const newChoice = { id: story.choices.length + 1, text: '', nextPart: '' };
    setStory({ ...story, choices: [...story.choices, newChoice] });
  };

  const removeChoice = (index) => {
    const choices = story.choices.filter((_, i) => i !== index);
    setStory({ ...story, choices });
  };

  return (
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
  );
};

export default InteractiveStoryEditor;