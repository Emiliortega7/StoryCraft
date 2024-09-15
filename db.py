from sqlalchemy import create_engine, Column, Integer, String, DateTime, MetaData, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

Base = declarative_base()

class ExampleModel(Base):
    __tablename__ = 'example'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class DatabaseManager:
    def __init__(self):
        self.engine = None
        self.session = None

    def initialize_db(self):
        try:
            DATABASE_URL = os.getenv("DATABASE_URL")
            self.engine = create_engine(DATABASE_URL, echo=True)
            Base.metadata.create_all(self.engine)
            print("Database and tables initialized.")
        except SQLAlchemyError as e:
            print(f"Error initializing database: {e}")

    def get_session(self):
        if not self.session:
            DBSession = scoped_session(sessionmaker(bind=self.engine))
            self.session = DBSession()
        return self.session

    def close_session(self):
        if self.session:
            self.session.close()

    # New method to query entries by name
    def query_entries_by_name(self, name):
        session = self.get_session()
        try:
            result = session.query(ExampleModel).filter(or_(ExampleModel.name == name)).all()
            return result
        except SQLAlchemyError as e:
            print(f"Query error: {e}")
            session.rollback()
            return None

if __name__ == "__main__":
    db_manager = DatabaseManager()
    db_manager.initialize_db()

    # Adding a new entry
    session = db_manager.get_session()
    new_entry = ExampleModel(name="Example Entry")
    session.add(new_entry)
    try:
        session.commit()
        print("New entry added.")
    except SQLAlchemyError as e:
        print(f"Error adding entry: {e}")
        session.rollback()
    finally:
        db_manager.close_session()

    # Querying entries by name
    queried_entries = db_manager.query_entries_by_name("Example Entry")
    if queried_entries:
        for entry in queried_entries:
            print(f"Queried Entry: ID: {entry.id} | Name: {entry.name} | Created at: {entry.created_at}")