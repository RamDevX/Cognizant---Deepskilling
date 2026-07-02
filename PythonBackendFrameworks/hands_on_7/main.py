from fastapi import FastAPI, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import Course
from schemas import CourseCreate, CourseResponse

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Course Management API",
    description="Hands-On 7 - FastAPI CRUD API",
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


@app.get(
    "/api/courses/",
    response_model=list[CourseResponse],
    tags=["Courses"]
)
async def get_courses(db: Session = Depends(get_db)):
    return db.query(Course).all()



@app.get(
    "/api/courses/{course_id}",
    response_model=CourseResponse,
    tags=["Courses"]
)
async def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(
        Course.id == course_id
    ).first()

    if not course:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    return course



@app.post(
    "/api/courses/",
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



@app.put(
    "/api/courses/{course_id}",
    response_model=CourseResponse,
    tags=["Courses"]
)
async def update_course(
    course_id: int,
    updated_course: CourseCreate,
    db: Session = Depends(get_db)
):
    course = db.query(Course).filter(
        Course.id == course_id
    ).first()

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



@app.delete(
    "/api/courses/{course_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Courses"]
)
async def delete_course(
    course_id: int,
    db: Session = Depends(get_db)
):
    course = db.query(Course).filter(
        Course.id == course_id
    ).first()

    if not course:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    db.delete(course)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)