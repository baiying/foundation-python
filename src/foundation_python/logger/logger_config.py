import os
from dotenv import load_dotenv

load_dotenv()
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_DIR = os.getenv('LOG_DIR', '/Users/evan/Code/logs/foundation-python')

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)
