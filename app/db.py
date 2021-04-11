from databases import Database
from api.settings import settings

uri = f"mysql://{settings.db_username}:{settings.db_password}@{settings.db_url}/{settings.db_db}"
database = Database(uri)