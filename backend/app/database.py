import os
from pathlib import Path
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Explicitly point to the .env file location in backend/
BASE_DIR = Path(__file__).resolve().parent.parent  # goes up to backend/
load_dotenv(BASE_DIR / ".env")

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://127.0.0.1:27017")
DB_NAME     = os.getenv("DB_NAME", "codeanalyzer")

client = AsyncIOMotorClient(MONGODB_URL)
db     = client[DB_NAME]

users_col       = db["users"]
projects_col    = db["projects"]
analyses_col    = db["analyses"]
annotations_col = db["annotations"]
bookings_col    = db["bookings"]


async def ping_database() -> tuple[bool, str | None]:
    """Verify that MongoDB connection is active and healthy."""
    try:
        await client.admin.command("ping")
        return True, None
    except Exception as e:
        err = str(e)
        print(f"MongoDB connection error: {err}")
        return False, err


def get_db():
    """Return the current database instance."""
    return db


def get_client():
    """Return the Motor client instance."""
    return client
