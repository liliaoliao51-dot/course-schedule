from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import courses, seed

Base.metadata.create_all(bind=engine)

app = FastAPI(title="课表管理系统")

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
