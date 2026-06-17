USE college_db;

SELECT
    s.student_id,
    s.first_name,
    s.last_name,
    COUNT(e.course_id) AS courses_enrolled
FROM students s
JOIN enrollments e
    ON s.student_id = e.student_id
GROUP BY s.student_id, s.first_name, s.last_name
HAVING COUNT(e.course_id) >
(
    SELECT AVG(enrollment_count)
    FROM
    (
        SELECT COUNT(*) AS enrollment_count
        FROM enrollments
        GROUP BY student_id
    ) avg_table
);


SELECT c.course_name, c.course_code
FROM courses c
WHERE NOT EXISTS
(
    SELECT 1
    FROM enrollments e
    WHERE e.course_id = c.course_id
    AND e.grade <> 'A'
);


SELECT
    p.prof_name,
    p.salary,
    p.department_id
FROM professors p
WHERE p.salary =
(
    SELECT MAX(p2.salary)
    FROM professors p2
    WHERE p2.department_id = p.department_id
);


SELECT *
FROM
(
    SELECT
        d.department_id,
        d.dept_name,
        AVG(p.salary) AS avg_salary
    FROM departments d
    JOIN professors p
        ON d.department_id = p.department_id
    GROUP BY d.department_id,d.dept_name
) dept_avg
WHERE avg_salary > 85000;


DROP VIEW IF EXISTS vw_student_enrollment_summary;
DROP VIEW IF EXISTS vw_course_stats;


CREATE VIEW vw_student_enrollment_summary AS
SELECT
    s.student_id,
    CONCAT(s.first_name,' ',s.last_name) AS student_name,
    d.dept_name,
    COUNT(e.course_id) AS total_courses,
    ROUND(
        AVG(
            CASE
                WHEN e.grade='A' THEN 4
                WHEN e.grade='B' THEN 3
                WHEN e.grade='C' THEN 2
                WHEN e.grade='D' THEN 1
                WHEN e.grade='F' THEN 0
            END
        ),
        2
    ) AS gpa
FROM students s
LEFT JOIN departments d
    ON s.department_id=d.department_id
LEFT JOIN enrollments e
    ON s.student_id=e.student_id
GROUP BY s.student_id,student_name,d.dept_name;


CREATE VIEW vw_course_stats AS
SELECT
    c.course_name,
    c.course_code,
    COUNT(e.enrollment_id) AS total_enrollments,
    ROUND(
        AVG(
            CASE
                WHEN e.grade='A' THEN 4
                WHEN e.grade='B' THEN 3
                WHEN e.grade='C' THEN 2
                WHEN e.grade='D' THEN 1
                WHEN e.grade='F' THEN 0
            END
        ),
        2
    ) AS avg_gpa
FROM courses c
LEFT JOIN enrollments e
    ON c.course_id=e.course_id
GROUP BY c.course_id,c.course_name,c.course_code;


SELECT *
FROM vw_student_enrollment_summary
WHERE gpa > 3.0;


UPDATE vw_student_enrollment_summary
SET dept_name='Computer Science'
WHERE student_id=1;

DROP VIEW IF EXISTS vw_student_enrollment_summary;
DROP VIEW IF EXISTS vw_course_stats;

CREATE VIEW vw_student_enrollment_summary AS
SELECT
    student_id,
    first_name,
    last_name,
    enrollment_year
FROM students
WHERE enrollment_year >= 2022
WITH CHECK OPTION;

SELECT * FROM vw_student_enrollment_summary;

DROP PROCEDURE IF EXISTS sp_enroll_student;

DELIMITER $$

CREATE PROCEDURE sp_enroll_student
(
    IN p_student_id INT,
    IN p_course_id INT,
    IN p_enrollment_date DATE
)
BEGIN

    IF EXISTS
    (
        SELECT 1
        FROM enrollments
        WHERE student_id=p_student_id
        AND course_id=p_course_id
    )
    THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT='Duplicate enrollment not allowed';
    ELSE

        INSERT INTO enrollments
        (
            student_id,
            course_id,
            enrollment_date,
            grade
        )
        VALUES
        (
            p_student_id,
            p_course_id,
            p_enrollment_date,
            NULL
        );

    END IF;

END$$

DELIMITER ;

CALL sp_enroll_student(1,3,'2026-06-17');


CREATE TABLE IF NOT EXISTS department_transfer_log
(
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    old_department INT,
    new_department INT,
    transfer_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

DROP PROCEDURE IF EXISTS sp_transfer_student;

DELIMITER $$

CREATE PROCEDURE sp_transfer_student
(
    IN p_student_id INT,
    IN p_new_department INT
)
BEGIN

    DECLARE old_dept INT;

    START TRANSACTION;

    SELECT department_id
    INTO old_dept
    FROM students
    WHERE student_id=p_student_id;

    UPDATE students
    SET department_id=p_new_department
    WHERE student_id=p_student_id;

    INSERT INTO department_transfer_log
    (
        student_id,
        old_department,
        new_department
    )
    VALUES
    (
        p_student_id,
        old_dept,
        p_new_department
    );

    COMMIT;

END$$

DELIMITER ;

CALL sp_transfer_student(1,2);

START TRANSACTION;

UPDATE students
SET department_id=99
WHERE student_id=2;

ROLLBACK;

START TRANSACTION;

INSERT INTO enrollments
(student_id,course_id,enrollment_date,grade)
VALUES
(2,2,CURDATE(),'A');

SAVEPOINT first_insert;

INSERT INTO enrollments
(student_id,course_id,enrollment_date,grade)
VALUES
(999,999,CURDATE(),'A');

ROLLBACK TO first_insert;

COMMIT;

SELECT * FROM enrollments;