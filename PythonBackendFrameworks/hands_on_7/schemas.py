from pydantic import BaseModel


class CourseBase(BaseModel):
    name: str
    code: str
    credits: int


class CourseCreate(CourseBase):
    pass


class CourseResponse(CourseBase):
    id: int

    class Config:
        from_attributes = True