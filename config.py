import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

class Config:
    # Secret key for session management and other security purposes
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')

    # Database URI for SQLAlchemy, defaulting to a local MySQL setup
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'SQLALCHEMY_DATABASE_URI',
        'mysql+pymysql://root:@localhost/healthcare_bot_db'
    )

    # Disable modification tracking to save resources
    SQLALCHEMY_TRACK_MODIFICATIONS = False
