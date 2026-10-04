import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import settings

# If DATABASE_URL starts with postgres://, convert to postgresql:// for SQLAlchemy 2.0
db_url = settings.DATABASE_URL
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)
elif os.getenv("VERCEL") and ("./blindspot.db" in db_url or db_url == "sqlite:///./blindspot.db"):
    db_url = "sqlite:////tmp/blindspot.db"

# Handle SQLite vs PostgreSQL engine arguments
connect_args = {}
if db_url.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    db_url,
    connect_args=connect_args,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

_initialized = False

def init_db():
    global _initialized
    import app.models.user
    import app.models.decision
    import app.models.analysis
    Base.metadata.create_all(bind=engine)
    _initialized = True

def get_db():
    global _initialized
    if not _initialized:
        try:
            init_db()
        except Exception:
            pass
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
