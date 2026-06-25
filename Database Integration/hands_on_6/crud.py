from sqlalchemy.orm import sessionmaker, joinedload
from models import engine, Student, Department, Course, Enrollment

Session = sessionmaker(bind=engine)
session = Session()

print("\nCREATE")

existing = session.query(Student).filter_by(
    email="rahul.sharma@example.com"
).first()

if not existing:
    new_student = Student(
        first_name="Rahul",
        last_name="Sharma",
        email="rahul.sharma@example.com",
        enrollment_year=2024,
        department_id=1
    )
    session.add(new_student)
    session.commit()
    print("Student inserted successfully.")
else:
    print("Student already exists.")

print("\nREAD ALL STUDENTS")

students = session.query(Student).all()

for student in students:
    print(
        student.student_id,
        student.first_name,
        student.last_name
    )

print("\nSTUDENTS IN COMPUTER SCIENCE")

cs_students = (
    session.query(Student)
    .join(Department)
    .filter(Department.dept_name == "Computer Science")
    .all()
)

for student in cs_students:
    print(student.first_name, student.last_name)

print("\nENROLLMENTS")

enrollments = session.query(Enrollment).all()

for enrollment in enrollments:
    print(
        enrollment.student.first_name,
        "->",
        enrollment.course.course_name
    )

print("\nUPDATE")

student = session.query(Student).filter_by(
    email="rahul.sharma@example.com"
).first()

if student:
    student.enrollment_year = 2025
    session.commit()
    print("Student updated successfully.")

print("\nDELETE ENROLLMENT")

enrollment = session.query(Enrollment).first()

if enrollment:
    session.delete(enrollment)
    session.commit()
    print("One enrollment deleted.")

print("\n========== N+1 QUERY ==========")

enrollments = session.query(Enrollment).all()

for enrollment in enrollments:
    print(
        enrollment.student.first_name,
        "-",
        enrollment.course.course_name
    )

print("\nJOINEDLOAD ")

enrollments = (
    session.query(Enrollment)
    .options(
        joinedload(Enrollment.student),
        joinedload(Enrollment.course)
    )
    .all()
)

for enrollment in enrollments:
    print(
        enrollment.student.first_name,
        "-",
        enrollment.course.course_name
    )

print("""
Observation:
Without joinedload(), SQLAlchemy executes additional queries
for each related student and course (N+1 problem).

Using joinedload(), related data is fetched using JOINs,
reducing the number of SQL queries and improving performance.
""")

session.close()