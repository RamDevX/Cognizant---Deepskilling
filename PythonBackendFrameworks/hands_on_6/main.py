from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import Base, SessionLocal, engine
from models import Course as CourseModel
from schemas import Course, CourseCreate

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Course Management API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/courses", response_model=list[Course])
def get_courses(db: Session = Depends(get_db)):
    return db.query(CourseModel).all()


@app.get("/courses/{course_id}", response_model=Course)
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(CourseModel).filter(
        CourseModel.id == course_id
    ).first()

    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    return course


@app.post("/courses", response_model=Course)
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    new_course = CourseModel(**course.model_dump())

    db.add(new_course)
    db.commit()
    db.refresh(new_course)

    return new_course


@app.put("/courses/{course_id}", response_model=Course)
def update_course(course_id: int, updated: CourseCreate,
                  db: Session = Depends(get_db)):
    course = db.query(CourseModel).filter(
        CourseModel.id == course_id
    ).first()

    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    course.name = updated.name
    course.code = updated.code
    course.credits = updated.credits

    db.commit()
    db.refresh(course)

    return course


@app.delete("/courses/{course_id}")
def delete_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(CourseModel).filter(
        CourseModel.id == course_id
    ).first()

    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    db.delete(course)
    db.commit()

    return {"message": "Course deleted successfully"}