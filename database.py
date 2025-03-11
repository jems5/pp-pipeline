from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

database_url = os.getenv("DATABASE_URL", "postgresql://default_user:default_password@localhost:5432/default_db")
engine = create_engine(database_url, echo=True)

## postgres://{username}:{password}@{host}/{database}
## if dbeaver connection failed, try initiating postgres database in terminal first

Base = declarative_base()
Session = sessionmaker()

