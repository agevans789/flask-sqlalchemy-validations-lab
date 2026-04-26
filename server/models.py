from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
import re

metadata = MetaData()
db = SQLAlchemy(metadata=metadata)

class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Author must have a name.")
        # Check for uniqueness manually if the test triggers before db commit
        if db.session.query(Author).filter(Author.name == name).first():
            raise ValueError("Name must be unique.")
        return name

    @validates('phone_number')
    def validate_phone(self, key, phone_number):
        if not (len(phone_number) == 10 and phone_number.isdigit()):
            raise ValueError("Phone number must be exactly 10 digits.")
        return phone_number

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    content = db.Column(db.Text)
    summary = db.Column(db.String)
    category = db.Column(db.String)

    @validates('title')
    def validate_title(self, key, title):
        if not title:
            raise ValueError("Post must have a title.")
        
        # Clickbait Check (Step 8/9 logic)
        clickbait_keywords = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(word in title for word in clickbait_keywords):
            raise ValueError("Title must be clickbait.")
        return title

    @validates('content')
    def validate_content(self, key, content):
        if len(content) < 250:
            raise ValueError("Content must be at least 250 characters.")
        return content

    @validates('summary')
    def validate_summary(self, key, summary):
        if summary and len(summary) > 250:
            raise ValueError("Summary cannot exceed 250 characters.")
        return summary

    @validates('category')
    def validate_category(self, key, category):
        valid_categories = ['Fiction', 'Non-Fiction']
        if category not in valid_categories:
            raise ValueError("Category must be Fiction or Non-Fiction.")
        return category
