import sqlite3
import os
from app.core.config import DB_PATH, DB_URL


def init_sqlite_db():
    """Initialize SQLite database with schema if it doesn't exist."""

    # Ensure database directory exists
    db_dir = os.path.dirname(DB_PATH) or "."
    os.makedirs(db_dir, exist_ok=True)

    schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")

    try:
        with sqlite3.connect(DB_PATH) as conn:
            with open(schema_path, "r", encoding="utf-8") as f:
                sql_script = f.read()
                conn.executescript(sql_script)
                conn.commit()
        return True
    except Exception as e:
        print(f"Error initializing database: {e}")
        return False


def init_sqlalchemy_db():
    """Initialize SQLAlchemy engine and create tables."""
    try:
        from app.models.entities import Base
        from sqlalchemy import create_engine

        # For SQLite, we need to extract the file path from the URL
        db_path = DB_URL.replace("sqlite:///", "")
        os.makedirs(os.path.dirname(db_path) or ".", exist_ok=True)

        engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
        Base.metadata.create_all(bind=engine)
        return True
    except Exception as e:
        print(f"Error creating SQLAlchemy tables: {e}")
        return False


def verify_database():
    """Verify database is initialized and ready."""
    try:
        import sqlite3

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Check if expenses table exists
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='expenses'"
        )
        exists = cursor.fetchone() is not None
        conn.close()

        return exists
    except Exception as e:
        print(f"Error verifying database: {e}")
        return False
