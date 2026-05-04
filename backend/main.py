import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from backend.database import engine, Base, DATABASE_URL
from backend.routers import courses, seed

# 如果旧数据库表结构和当前 model 不一致，自动删除重建（仅 SQLite）
if DATABASE_URL.startswith("sqlite"):
    DB_PATH = os.path.join(os.path.dirname(__file__), "courses.db")
    if os.path.exists(DB_PATH):
        import sqlalchemy
        insp = sqlalchemy.inspect(engine)
        if insp.has_table("courses"):
            existing = {col["name"] for col in insp.get_columns("courses")}
            required = {"name", "classroom", "day_of_week", "start_period", "duration", "teacher", "start_time", "end_time"}
            if not required.issubset(existing):
                os.remove(DB_PATH)
                print("⚠️  检测到旧数据库表结构不匹配，已自动删除 courses.db，将重新创建。")

# 自动创建所有表
Base.metadata.create_all(bind=engine)

app = FastAPI(title="课表管理系统")

# CORS 配置 - 允许所有来源访问（开发阶段）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(courses.router)
app.include_router(seed.router)


@app.get("/")
def root():
    return {"message": "课表管理系统 API"}


@app.get("/health")
def health_check():
    return {"status": "ok"}
