from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    Response,
    status
)
from sqlalchemy.orm import Session
from sqlalchemy import or_

from database import Base, engine, get_db
from models import Course
from schemas import (
    CourseCreate,
    CourseUpdate,
    CourseResponse
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Course Management API",
    description="Hands-On 8 - REST API Best Practices",
    version="1.0.0",
    contact={
        "name": "Raxon",
        "email": "example@example.com"
    }
)


@app.get("/")
async def home():
    return {
        "message": "Welcome to Course Management API"
    }


# GET ALL COURSES (Pagination + Search)
@app.get(
    "/api/v1/courses/",
    response_model=list[CourseResponse],
    tags=["Courses"]
)
async def get_courses(
    page: int = 1,
    page_size: int = 10,
    search: str | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(Course)

    if search:
        query = query.filter(
            or_(
                Course.name.contains(search),
                Course.code.contains(search)
            )
        )

    return query.offset((page - 1) * page_size).limit(page_size).all()


# GET COURSE BY ID
@app.get(
    "/api/v1/courses/{course_id}",
    response_model=CourseResponse,
    tags=["Courses"]
)
async def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()

    if not course:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    return course


# CREATE COURSE
@app.post(
    "/api/v1/courses/",
    response_model=CourseResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Courses"],
    summary="Create a new course"
)
async def create_course(
    course: CourseCreate,
    db: Session = Depends(get_db)
):
    new_course = Course(**course.model_dump())

    db.add(new_course)
    db.commit()
    db.refresh(new_course)

    return new_course


# UPDATE COURSE
@app.put(
    "/api/v1/courses/{course_id}",
    response_model=CourseResponse,
    tags=["Courses"]
)
async def update_course(
    course_id: int,
    updated_course: CourseCreate,
    db: Session = Depends(get_db)
):
    course = db.query(Course).filter(Course.id == course_id).first()

    if not course:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    course.name = updated_course.name
    course.code = updated_course.code
    course.credits = updated_course.credits

    db.commit()
    db.refresh(course)

    return course


# PARTIAL UPDATE
@app.patch(
    "/api/v1/courses/{course_id}",
    response_model=CourseResponse,
    tags=["Courses"]
)
async def patch_course(
    course_id: int,
    updated_course: CourseUpdate,
    db: Session = Depends(get_db)
):
    course = db.query(Course).filter(Course.id == course_id).first()

    if not course:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    data = updated_course.model_dump(exclude_unset=True)

    for key, value in data.items():
        setattr(course, key, value)

    db.commit()
    db.refresh(course)

    return course


# DELETE COURSE
@app.delete(
    "/api/v1/courses/{course_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Courses"]
)
async def delete_course(
    course_id: int,
    db: Session = Depends(get_db)
):
    course = db.query(Course).filter(Course.id == course_id).first()

    if not course:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    db.delete(course)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)