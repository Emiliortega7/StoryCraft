from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()

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

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

if __name__ == "__main__":
    app.run(debug=True)