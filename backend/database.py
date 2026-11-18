import os
from urllib.parse import quote_plus
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

raw_database_url = os.getenv("DATABASE_URL")
engine = None
SessionLocal = None
Base = declarative_base()

def init_db():
    global engine, SessionLocal
    if raw_database_url:
        target_url = raw_database_url
        if target_url.startswith("postgres://"):
            target_url = target_url.replace("postgres://", "postgresql://", 1)
        try:
            temp_engine = create_engine(target_url, echo=False)
            with temp_engine.connect() as conn:
                pass
            engine = temp_engine
            SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
            return
        except Exception:
            pass

    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "3306")
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_NAME = os.getenv("DB_NAME", "intelligent_product_recommendation")

    if DB_PASSWORD:
        mysql_url = (
            f"mysql+pymysql://{DB_USER}:{quote_plus(DB_PASSWORD)}"
            f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )
        try:
            temp_engine = create_engine(mysql_url, echo=False)
            with temp_engine.connect() as conn:
                pass
            engine = temp_engine
            SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
            return
        except Exception:
            # Fallback gracefully to SQLite if MySQL is unreachable or not started
            pass

    # Resilient local SQLite fallback
    sqlite_url = "sqlite:///./intelligent_recommendation.db"
    engine = create_engine(sqlite_url, connect_args={"check_same_thread": False}, echo=False)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

init_db()
