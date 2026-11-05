import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a-very-long-random-string-for-local-dev-only'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///portfolio.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
    
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB