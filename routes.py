from flask import Flask, request, jsonify
import json
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

available_stories = [{
    "id": 1,
    "title": "The Adventure Begins",
    "content": "Your adventure starts in a small town..."
}]

story_choices = [{
    "id": 1,
    "story_id": 1,
    "description": "Enter the forest",
    "next_story_id": 2
}]

def get_story_by_id(story_id):
    return next((story for story in available_stories if story["id"] == story_id), None)

def get_choice_by_id(choice_id):
    return next((choice for choice in story_choices if choice["id"] == choice_id), None)

@app.route('/stories', methods=['GET', 'POST'])
def stories_operations():
    if request.method == 'GET':
        return jsonify(available_stories)
    elif request.method == 'POST':
        data = request.get_json()
        new_story = {
            "id": len(available_stories) + 1,
            "title": data['title'],
            "content": data['content']
        }
        available_stories.append(new_story)
        return jsonify(new_story), 201

@app.route('/stories/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def manage_story(id):
    story = get_story_by_id(id)
    if request.method == 'GET':
        return jsonify(story) if story else ("Story not found", 404)
    elif request.method == 'PUT':
        if story:
            data = request.get_json()
            story.update({
                'title': data.get('title', story['title']),
                'content': data.get('content', story['content'])
            })
            return jsonify(story)
        else:
            return "Story not found", 404
    elif request.method == 'DELETE':
        if story:
            available_stories.remove(story)
            return '', 204
        else:
            return "Story not found", 404

@app.route('/choices', methods=['GET', 'POST'])
def choices_operations():
    if request.method == 'GET':
        return jsonify(story_choices)
    elif request.method == 'POST':
        data = request.get_json()
        new_choice = {
            "id": len(story_choices) + 1,
            "story_id": data['story_id'],
            "description": data['description'],
            "next_story_id": data['next_story_id']
        }
        story_choices.append(new_choice)
        return jsonify(new_choice), 201

@app.route('/choices/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def manage_choice(id):
    choice = get_choice_by_id(id)
    if request.method == 'GET':
        return jsonify(choice) if choice else ("Choice not found", 404)
    elif request.method == 'PUT':
        if choice:
            data = request.get_json()
            choice.update({
                'story_id': data.get('story_id', choice['story_id']),
                'description': data.get('description', choice['description']),
                'next_story_id': data.get('next_story_id', choice['next_story_id'])
            })
            return jsonify(choice)
        else:
            return "Choice not found", 404
    elif request.method == 'DELETE':
        if choice:
            story_choices.remove(choice)
            return '', 204
        else:
            return "Choice not found", 404

if __name__ == '__main__':
    app.run(debug=True)