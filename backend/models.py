from sqlalchemy import Column, Integer, String
from database import Base


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)          # 课程名
    classroom = Column(String, nullable=False)      # 教室
    day_of_week = Column(Integer, nullable=False)   # 周几 (1=周一, 7=周日)
    start_period = Column(Integer, nullable=False)  # 起始节次
    duration = Column(Integer, nullable=False)      # 持续节次
    teacher = Column(String, nullable=True, default="")  # 授课老师
