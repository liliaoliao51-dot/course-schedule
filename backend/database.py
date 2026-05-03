import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 本地开发用 SQLite，部署时用 DATABASE_URL（Railway 会自动设置 PostgreSQL）
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./courses.db")

# Railway 的 PostgreSQL URL 以 postgres:// 开头，SQLAlchemy 需要 postgresql://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# SQLite 需要 check_same_thread=False，PostgreSQL 不需要
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
