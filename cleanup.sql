-- Temporarily disable foreign key checks
SET session_replication_role = 'replica';

-- Clear all tables in the correct order
TRUNCATE TABLE enrolls_in CASCADE;
TRUNCATE TABLE course_offering CASCADE;
TRUNCATE TABLE course CASCADE;
TRUNCATE TABLE student CASCADE;
TRUNCATE TABLE teacher CASCADE;
TRUNCATE TABLE "user" CASCADE;
TRUNCATE TABLE department CASCADE;
TRUNCATE TABLE semester CASCADE;

-- Re-enable foreign key checks
SET session_replication_role = 'origin';

-- Reset all sequences
ALTER SEQUENCE IF EXISTS department_department_id_seq RESTART WITH 1;
ALTER SEQUENCE IF EXISTS "user_user_id_seq" RESTART WITH 1;
ALTER SEQUENCE IF EXISTS teacher_teacher_id_seq RESTART WITH 1;
ALTER SEQUENCE IF EXISTS student_student_id_seq RESTART WITH 1;
ALTER SEQUENCE IF EXISTS course_course_id_seq RESTART WITH 1;
ALTER SEQUENCE IF EXISTS course_offering_id_seq RESTART WITH 1;
ALTER SEQUENCE IF EXISTS semester_semester_id_seq RESTART WITH 1; 