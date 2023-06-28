import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.models import Base

# Load environment variables from .env file
dotenv_path = os.path.join(os.path.dirname(__file__), "..", "secrets", ".env")


class DatabaseSetup:
    def __init__(self):
        load_dotenv(dotenv_path)
        self.db_uri = self.create_db_uri()
        self.session = self.create_session()

    def create_db_uri(self):
        db_host = os.environ.get("DB_HOST")
        db_port = os.environ.get("DB_PORT")
        db_name = os.environ.get("DB_NAME")
        db_user = os.environ.get("DB_USER")
        db_password = os.environ.get("DB_PASSWORD")
        return f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

    def create_session(self):
        engine = create_engine(self.db_uri)
        session = sessionmaker(bind=engine)
        Base.metadata.create_all(engine)
        return session()
