USE college_db;

-- =====================================================
-- HANDS-ON 4
-- Query Optimization, Indexes & EXPLAIN
-- =====================================================

-- =====================================================
-- TASK 1 : BASELINE PERFORMANCE (NO INDEXES)
-- =====================================================

-- 48
-- Run EXPLAIN FORMAT=JSON on the query

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

-- 49 & 50
-- Document observations from the output:
-- Check whether any table uses:
-- "access_type": "ALL"
-- which indicates a full table scan.
-------------------------------------

-- Note estimated rows examined.

-- =====================================================
-- TASK 2 : ADD INDEXES
-- =====================================================

-- 51
CREATE INDEX idx_students_enrollment_year
ON students(enrollment_year);

-- 52
CREATE UNIQUE INDEX idx_enrollments_student_course
ON enrollments(student_id, course_id);

-- 53
CREATE INDEX idx_courses_course_code
ON courses(course_code);

-- 54
-- Re-run EXPLAIN and compare with baseline

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

-- Comment your findings:
-- Full Table Scan -> Index Scan?
-- Rows examined reduced?

-- 55
-- MySQL does not support PostgreSQL-style partial indexes.
-- Closest practical equivalent:

CREATE INDEX idx_enrollments_grade_student
ON enrollments(grade, student_id);

-- Test query benefiting from the index

EXPLAIN FORMAT=JSON
SELECT *
FROM enrollments
WHERE grade IS NULL;

-- =====================================================
-- TASK 3 : N+1 QUERY PROBLEM DEMONSTRATION
-- =====================================================

-- Simulated N+1 approach

SELECT *
FROM enrollments;

-- Then for each enrollment:
-- SELECT first_name,last_name
-- FROM students
-- WHERE student_id=?;

-- Better approach using JOIN

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

-- =====================================================
-- INDEX VERIFICATION
-- =====================================================

SHOW INDEX FROM students;

SHOW INDEX FROM enrollments;

SHOW INDEX FROM courses;

-- =====================================================
-- TEST DUPLICATE ENROLLMENT PROTECTION
-- =====================================================

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

-- Expected:
-- Error due to UNIQUE index
-- idx_enrollments_student_course

-- =====================================================
-- PERFORMANCE CHECKS
-- =====================================================

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
