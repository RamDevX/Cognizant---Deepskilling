USE college_db;

EXPLAIN FORMAT=JSON
SELECT
s.first_name,
s.last_name,
c.course_name
FROM enrollments e
JOIN students s
ON s.student_id = e.student_id
JOIN courses c
ON c.course_id = e.course_id
WHERE s.enrollment_year = 2022;

CREATE INDEX idx_students_enrollment_year
ON students(enrollment_year);

CREATE UNIQUE INDEX idx_enrollments_student_course
ON enrollments(student_id, course_id);

CREATE INDEX idx_courses_course_code
ON courses(course_code);

EXPLAIN FORMAT=JSON
SELECT
s.first_name,
s.last_name,
c.course_name
FROM enrollments e
JOIN students s
ON s.student_id = e.student_id
JOIN courses c
ON c.course_id = e.course_id
WHERE s.enrollment_year = 2022;


CREATE INDEX idx_enrollments_grade_student
ON enrollments(grade, student_id);


EXPLAIN FORMAT=JSON
SELECT *
FROM enrollments
WHERE grade IS NULL;


SELECT *
FROM enrollments;


SELECT
e.enrollment_id,
s.first_name,
s.last_name,
c.course_name,
e.grade
FROM enrollments e
JOIN students s
ON e.student_id = s.student_id
JOIN courses c
ON e.course_id = c.course_id;


SHOW INDEX FROM students;

SHOW INDEX FROM enrollments;

SHOW INDEX FROM courses;


INSERT INTO enrollments
(
student_id,
course_id,
enrollment_date,
grade
)
VALUES
(
1,
1,
CURDATE(),
'A'
);


EXPLAIN
SELECT *
FROM students
WHERE enrollment_year = 2022;

EXPLAIN
SELECT *
FROM courses
WHERE course_code = 'CS101';

EXPLAIN
SELECT *
FROM enrollments
WHERE student_id = 1
AND course_id = 1;
