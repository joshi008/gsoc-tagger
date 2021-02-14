from dotenv import load_dotenv
load_dotenv()

from pathlib import Path  # Python 3.6+ only
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

import os
MONGO_URI = os.getenv("MONGO_URI")