import os
from dotenv import load_dotenv

# Загружаем переменные из .env (локально)
basedir = os.path.abspath(os.path.dirname(__file__))
env_path = os.path.join(basedir, '..', '.env')
load_dotenv(dotenv_path=env_path)

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-key")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
