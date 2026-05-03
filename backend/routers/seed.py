from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import models

router = APIRouter(prefix="/api/seed", tags=["seed"])


@router.post("/")
def seed_courses(db: Session = Depends(get_db)):
    """清空并预填测试课程数据"""
    db.query(models.Course).delete()
    db.commit()

    courses = [
        models.Course(name="高等数学",     classroom="教学楼A-301",     day_of_week=1, start_period=1, duration=2, teacher="张明", start_time="08:00", end_time="09:40"),
        models.Course(name="大学英语",     classroom="外语楼B-205",     day_of_week=1, start_period=5, duration=2, teacher="李华", start_time="14:00", end_time="15:40"),
        models.Course(name="数据结构",     classroom="计算机楼C-102",   day_of_week=2, start_period=3, duration=2, teacher="王强", start_time="10:00", end_time="11:40"),
        models.Course(name="体育",         classroom="体育馆",         day_of_week=2, start_period=7, duration=2, teacher="赵刚", start_time="16:00", end_time="17:40"),
        models.Course(name="线性代数",     classroom="教学楼A-405",     day_of_week=3, start_period=1, duration=2, teacher="张明", start_time="08:00", end_time="09:40"),
        models.Course(name="思政课",       classroom="综合楼D-301",     day_of_week=3, start_period=5, duration=3, teacher="刘芳", start_time="14:00", end_time="16:45"),
        models.Course(name="大学英语",     classroom="外语楼B-205",     day_of_week=4, start_period=1, duration=2, teacher="李华", start_time="08:00", end_time="09:40"),
        models.Course(name="数据结构实验", classroom="计算机楼C-机房3", day_of_week=4, start_period=3, duration=3, teacher="王强", start_time="10:00", end_time="12:30"),
        models.Course(name="高等数学",     classroom="教学楼A-301",     day_of_week=5, start_period=1, duration=2, teacher="张明", start_time="08:00", end_time="09:40"),
        models.Course(name="选修：摄影",   classroom="艺术楼E-101",     day_of_week=5, start_period=5, duration=2, teacher="陈艺", start_time="14:00", end_time="15:40"),
    ]

    db.add_all(courses)
    db.commit()

    return {"message": f"已写入 {len(courses)} 条测试课程"}
