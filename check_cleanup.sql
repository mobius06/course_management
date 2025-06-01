-- Check table counts
SELECT 'department' as table_name, COUNT(*) as record_count FROM department
UNION ALL
SELECT 'user', COUNT(*) FROM "user"
UNION ALL
SELECT 'teacher', COUNT(*) FROM teacher
UNION ALL
SELECT 'student', COUNT(*) FROM student
UNION ALL
SELECT 'course', COUNT(*) FROM course
UNION ALL
SELECT 'course_offering', COUNT(*) FROM course_offering
UNION ALL
SELECT 'enrolls_in', COUNT(*) FROM enrolls_in
UNION ALL
SELECT 'semester', COUNT(*) FROM semester
ORDER BY table_name;

-- Check sequence values
WITH sequence_info AS (
    SELECT 
        sequence_name,
        start_value,
        minimum_value,
        maximum_value,
        increment
    FROM information_schema.sequences
    WHERE sequence_schema = 'public'
)
SELECT 
    sequence_name,
    start_value,
    minimum_value,
    maximum_value,
    increment
FROM sequence_info
ORDER BY sequence_name; 