import os

from dotenv import load_dotenv
load_dotenv()

current_directory = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(current_directory, '..'))

dateBaseConfig = {
    'dbhost': os.getenv('DB_HOST'),
    'name': os.getenv('DB_NAME'),
    'dbport': 3306,
    'dppass': os.getenv('DB_PASSWORD'),
    'dbname': os.getenv('DB_SCHEME'),
}


class Settings():
    bot_token = os.getenv('BOT_TOKEN')
    

config = Settings()