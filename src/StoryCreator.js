import React, { useState, useCallback } from 'react';

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, errorInfo: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, errorInfo: error };
  }

  componentDidCatch(error, info) {
    console.log(error, info);
  }

  render() {
    if (this.state.hasError) {
      return <h1>An error occurred in the application.</h1>;
    }

    return this.props.children; 
  }
}

const StoryEditor = () => {
  const [storyData, setStoryData] = useState({
    title: '',
    narrative: '',
    decisions: [{ id: 1, option: '', followUp: '' }],
  });

  const handleStoryChange = useCallback((e) => {
    const { name, value } = e.target;
    try {
      setStoryData({ ...storyData, [name]: value });
    } catch (error) {
      console.error("Failed to update story data:", error);
    }
  }, [storyData]);

  const handleDecisionChange = useCallback((decisionIndex, e) => {
    const { name, value } = e.target;
    try {
      const updatedDecisions = [...storyData.decisions];
      updatedDecisions[decisionIndex] = { ...updatedDecisions[decisionIndex], [name]: value };
      setStoryData({ ...storyData, decisions: updatedDecisions });
    } catch (error) {
      console.error(`Failed to update decision ${decisionIndex}:`, error);
    }
  }, [storyData]);

  const addNewDecision = useCallback(() => {
    try {
      const newDecision = { id: storyData.decisions.length + 1, option: '', followUp: '' };
      setStoryData({ ...storyData, decisions: [...storyData.decisions, newDecision] });
    } catch (error) {
      console.error("Failed to add new decision:", error);
    }
  }, [storyData]);

  const removeDecision = useCallback((decisionIndex) => {
    try {
      const filteredDecisions = storyData.decisions.filter((_, i) => i !== decisionIndex);
      setStoryData({ ...storyData, decisions: filteredDecisions });
    } catch (error) {
      console.error(`Failed to remove decision ${decisionIndex}:`, error);
    }
  }, [storyData]);

  return (
    <ErrorBoundary>
      <div>
        <h2>Interactive Story Creation/Editing Tool</h2>
        <form>
          <div>
            <label>Title:</label>
            <input
              type="text"
              name="title"
              value={storyData.title}
              onChange={handleStoryChange}
            />
          </div>
          <div>
            <label>Narrative:</label>
            <textarea
              name="narrative"
              value={storyData.narrative}
              onChange={handleStoryChange}
            />
          </div>
          {storyData.decisions.map((decision, index) => (
            <div key={decision.id}>
              <label>Decision {index + 1}:</label>
              <input
                type="text"
                name="option"
                value={decision.option}
                onChange={(e) => handleDecisionChange(index, e)}
              />
              <input
                type="text"
                name="followUp"
                value={decision.followUp}
                onChange={(e) => handleDecisionChange(index, e)}
              />
              <button type="button" onClick={() => removeDecision(index)}>Remove Decision</button>
            </div>
          ))}
          <button type="button" onClick={addNewDecision}>Add New Decision</button>
        </form>
      </div>
    </ErrorBoundary>
  );
};

export default StoryEditor;