import React, { useState } from 'react';

const stories = [
  {
    id: 1,
    text: "You're in a dark forest. Two paths lie ahead: left and right. Which one do you take?",
    choices: [
      { text: 'Left', leadsTo: 2 },
      { text: 'Right', leadsTo: 3 },
    ],
  },
  {
    id: 2,
    text: "You've encountered a friendly dragon! Do you talk to it or continue on your path?",
    choices: [
      { text: 'Talk', leadsTo: 4 },
      { text: 'Continue', leadsTo: 5 },
    ],
  },
  {
    id: 3,
    text: "You've found a magical river. Do you drink the water or rest beside it?",
    choices: [
      { text: 'Drink', leadsTo: 6 },
      { text: 'Rest', leadsTo: 7 },
    ],
  },
  { id: 4, text: "The dragon tells you a secret. The end.", choices: [] },
  { id: 5, text: "You find a hidden treasure. The end.", choices: [] },
  { id: 6, text: "You gain magical powers. The end.", choices: [] },
  { id: 7, text: "You have a refreshing nap and dream of adventures. The end.", choices: [] },
];

function StoryViewer() {
  const [currentStory, setCurrentStory] = useState(stories[0]);

  const selectChoice = (choiceId) => {
    const nextStory = stories.find(story => story.id === choiceId);
    if (nextStory) {
      setCurrentStory(nextStory);
    }
  };

  return (
    <div className="story-viewer">
      <p>{currentStory.text}</p>
      {currentStory.choices.length > 0 && (
        <div className="choices">
          {currentStory.choices.map((choice, index) => (
            <button key={index} onClick={() => selectChoice(choice.leadsTo)}>
              {choice.text}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}

export default StoryViewer;