from flask import Flask, request, jsonify
import os
import json
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)
stories = [{
    "id": 1,
    "title": "The Adventure Begins",
    "content": "Your adventure starts in a small town..."
}]
choices = [{
    "id": 1,
    "story_id": 1,
    "description": "Enter the forest",
    "next_story_id": 2
}]
@app.route('/stories', methods=['GET', 'POST'])
def handle_stories():
    if request.method == 'GET':
        return jsonify(stories)
    elif request.method == 'POST':
        data = request.get_json()
        new_story = {
            "id": len(stories) + 1,
            "title": data['title'],
            "content": data['content']
        }
        stories.append(new_story)
        return jsonify(new_story), 201
@app.route('/stories/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handle_story(id):
    story = next((item for item in stories if item["id"] == id), None)
    if request.method == 'GET':
        if story:
            return jsonify(story)
        else:
            return "Story not found", 404
    elif request.method == 'PUT':
        data = request.get_json()
        if story:
            story['title'] = data.get('title', story['title'])
            story['content'] = data.get('content', story['content'])
            return jsonify(story)
        else:
            return "Story not found", 404
    elif request.method == 'DELETE':
        if story:
            stories.remove(story)
            return '', 204
        else:
            return "Story not found", 404
@app.route('/choices', methods=['GET', 'POST'])
def handle_choices():
    if request.method == 'GET':
        return jsonify(choices)
    elif request.method == 'POST':
        data = request.get_json()
        new_choice = {
            "id": len(choices) + 1,
            "story_id": data['story_id'],
            "description": data['description'],
            "next_story_id": data['next_story_id']
        }
        choices.append(new_choice)
        return jsonify(new_choice), 201
@app.route('/choices/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handle_choice(id):
    choice = next((item for item in choices if item["id"] == id), None)
    if request.method == 'GET':
        if choice:
            return jsonify(choice)
        else:
            return "Choice not found", 404
    elif request.method == 'PUT':
        data = request.get_json()
        if choice:
            choice['story_id'] = data.get('story_id', choice['story_id'])
            choice['description'] = data.get('description', choice['description'])
            choice['next_story_id'] = data.get('next_story_id', choice['next_story_id'])
            return jsonify(choice)
        else:
            return "Choice not found", 404
    elif request.method == 'DELETE':
        if choice:
            choices.remove(choice)
            return '', 204
        else:
            return "Choice not found", 404
if __name__ == '__main__':
    app.run(debug=True)