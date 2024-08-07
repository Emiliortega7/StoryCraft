from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    stories = db.relationship('Story', backref='author', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.username

class Story(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    choices = db.relationship('Choice', backref='story', lazy=True)

    def __repr__(self):
        return '<Story %r>' % self.title

class Choice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    outcome = db.Column(db.Text, nullable=True)
    story_id = db.Column(db.Integer, db.ForeignKey('story.id'), nullable=False)

    def __repr__(self):
        return '<Choice %r>' % self.description

@app.before_first_request
def create_tables():
    try:
        db.create_all()
    except Exception as e:
        app.logger.error(f"Error creating tables: {e}")

@app.route('/stories', methods=['GET'])
def get_stories():
    try:
        stories = Story.query.all()
        return jsonify([{'title': story.title, 'content': story.content} for story in stories])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    try:
        app.run(debug=True)
    except Exception as e:
        print(f"Failed to start Flask application: {e}")