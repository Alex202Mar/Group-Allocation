
SUPERVISOR MAXIMUM CAPACITY
Supervisor.is_free()
    returns whether the supervisor is free or has reached max students
    (limits the supervisor capacity to max_students)

STUDENT GRADE PRIORITY
Supervisor._prefers(student_a, student_b)
    returns if the supervisor prefers student b than student a
    a supervisor prefers a student if:
        - it is in the priority list (lines 19, 21)
        - it requests the primary module of the supervisor and not one of the secondary modules (line 23)
        - has a better grading (`status_quo.total_score < new.total_score`, line 28)
