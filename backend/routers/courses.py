from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend import schemas
from backend import crud

router = APIRouter(prefix="/api/courses", tags=["courses"])


@router.get("", response_model=list[schemas.CourseOut])
def list_courses(db: Session = Depends(get_db)):
    return crud.get_courses(db)


@router.post("", response_model=schemas.CourseOut, status_code=201)
def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    return crud.create_course(db, course)


@router.get("/{course_id}", response_model=schemas.CourseOut)
def read_course(course_id: int, db: Session = Depends(get_db)):
    course = crud.get_course(db, course_id)
    if course is None:
        raise HTTPException(status_code=404, detail="课程不存在")
    return course


@router.put("/{course_id}", response_model=schemas.CourseOut)
def update_course(course_id: int, course: schemas.CourseUpdate, db: Session = Depends(get_db)):
    updated = crud.update_course(db, course_id, course)
    if updated is None:
        raise HTTPException(status_code=404, detail="课程不存在")
    return updated


@router.delete("/{course_id}", status_code=204)
def delete_course(course_id: int, db: Session = Depends(get_db)):
    if not crud.delete_course(db, course_id):
        raise HTTPException(status_code=404, detail="课程不存在")
