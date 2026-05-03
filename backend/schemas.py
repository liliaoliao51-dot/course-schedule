from pydantic import BaseModel, Field


class CourseBase(BaseModel):
    name: str = Field(..., min_length=1, description="课程名")
    classroom: str = Field(..., min_length=1, description="教室")
    day_of_week: int = Field(..., ge=1, le=7, description="周几 (1=周一, 7=周日)")
    start_period: int = Field(..., ge=1, description="起始节次")
    duration: int = Field(..., ge=1, description="持续节次")
    teacher: str = Field("", description="授课老师")
    start_time: str = Field("", description="开始时间 如 '08:00'")
    end_time: str = Field("", description="结束时间 如 '09:40'")


class CourseCreate(CourseBase):
    pass


class CourseUpdate(BaseModel):
    name: str | None = Field(None, min_length=1)
    classroom: str | None = Field(None, min_length=1)
    day_of_week: int | None = Field(None, ge=1, le=7)
    start_period: int | None = Field(None, ge=1)
    duration: int | None = Field(None, ge=1)
    teacher: str | None = None
    start_time: str | None = None
    end_time: str | None = None


class CourseOut(CourseBase):
    id: int

    class Config:
        from_attributes = True
