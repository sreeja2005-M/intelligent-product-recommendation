import os
from urllib.parse import quote_plus
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

raw_database_url = os.getenv("DATABASE_URL")

if raw_database_url:
    # Handle postgresql:// schema name for SQLAlchemy compatibility
    if raw_database_url.startswith("postgres://"):
        raw_database_url = raw_database_url.replace("postgres://", "postgresql://", 1)
    DATABASE_URL = raw_database_url
else:
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "3306")
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_NAME = os.getenv("DB_NAME", "intelligent_product_recommendation")
    
    if DB_PASSWORD:
        DATABASE_URL = (
            f"mysql+pymysql://{DB_USER}:{quote_plus(DB_PASSWORD)}"
            f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )
    else:
        # Fallback to local SQLite database if no MySQL password provided
        DATABASE_URL = "sqlite:///./intelligent_recommendation.db"

# Configure connect args for SQLite if used
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    echo=False
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()