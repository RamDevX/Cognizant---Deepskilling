from pydantic import BaseModel


class CourseBase(BaseModel):
    name: str
    code: str
    credits: int


class CourseCreate(CourseBase):
    pass


class CourseUpdate(BaseModel):
    name: str | None = None
    code: str | None = None
    credits: int | None = None


class CourseResponse(CourseBase):
    id: int

    class Config:
        from_attributes = True