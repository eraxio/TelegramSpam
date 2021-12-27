from sqlalchemy import create_engine
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

SESSIONS_PATH = Path(f"{BASE_DIR}/sessions/")
PROXIES_CSV_FILE = Path(f"{BASE_DIR}/proxies.csv")

engine = create_engine('sqlite:///db/sqlite3.db')
