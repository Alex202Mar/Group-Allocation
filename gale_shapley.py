from typing import List

from student import Student
from supervisor import Supervisor


"""
GALE-SHAPLEY ALGORITHM

algorithm stable_matching is
    Initialize all m ∈ M and w ∈ W to free
    while ∃ free man m who still has a woman w to propose to do
        w := first woman on m's list to whom m has not yet proposed
        if w is free then
            (m, w) become engaged
        else some pair (m', w) already exists
            if w prefers m to m' then
                m' becomes free
                (m, w) become engaged 
            else
                (m', w) remain engaged
            end if
        end if
    repeat
    
In this case, man are students, women are supervisors. 
"""


def gale_shapley(students: List[Student]) -> None:
    """ assigns all students to a supervisor """
    def stable_matching():
        """ :returns if a student (men) has still a supervisor to propose to (woman), not reached stability """
        return all([s.is_stable() for s in students])

    while not stable_matching():
        for student in students:
            if not student.has_preference():
                continue
            if not student.is_free():
                continue

            course_id, supervisor = student.preferences_supervisors.get()

            if supervisor.is_free():
                student.engage(supervisor, course_id)
                supervisor.engage(student, course_id)
                continue

            if supervisor.prefers(student, course_id):
                supervisor.free_one()
                student.engage(supervisor, course_id)
                supervisor.engage(student, course_id)
                continue

