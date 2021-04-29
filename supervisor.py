from dataclasses import dataclass, field
from typing import List, Tuple

from student import Student


@dataclass
class Supervisor:
    first_name: str
    last_name: str
    max_students: int
    modules: field(default_factory=tuple)
    id: str

    assigned_students: List[Tuple[str, Student]]

    def _prefers(self, status_quo: Student, status_quo_course_id: str, new: Student, new_course_id: str) -> bool:
        """ :returns wether new student is preferred """
        if self.id in new.priorities_in and self.id not in status_quo.priorities_in:
            return True  # new student is preferred because it is a supervisor priority
        if self.id in status_quo.priorities_in:
            return False  # if status quo is a supervisor priority, there is no possible way for the new to be better
        module_comparison = self.modules.index(status_quo_course_id) - self.modules.index(new_course_id)
        if module_comparison < 0:
            return False  # the status quo wants the supervisor's primary module and the new a secondary
        if module_comparison > 0:
            return True  # the new student wants the supervisor's primary module and the status quo a secondary
        if status_quo.total_score < new.total_score:
            return True  # the new student has a better score than the status quo student
        return False  # they are the same, no preference

    def prefers(self, new_student: Student, new_course_id: str) -> bool:
        """ :returns whether some engaged student is less qualified than new_student """
        for course_id, student in self.assigned_students:
            if self._prefers(student, course_id, new_student, new_course_id):
                return True
        return False

    def free_one(self):
        """ frees the least qualified student """
        least_qualified = None  # at the end of the loop, this will have the least qualified student
        for x in self.assigned_students:
            if least_qualified is None:
                least_qualified = x
                continue
            # if the current student is the new least qualified, save it as such
            course_id, student = x
            least_qualified_course_id, least_qualified_student = least_qualified
            if self._prefers(student, course_id, least_qualified_student, least_qualified_course_id):
                least_qualified = x

        if least_qualified is None:
            raise ValueError("unable to free one")

        # free the least qualified student
        self.assigned_students.remove(least_qualified)  # remove from assigned students
        least_qualified[1].un_engage()  # tell the student he has been dumped and is now unengaged

    def teaches(self, module_id):
        """ :returns whether this supervisor teaches this module """
        return module_id in self.modules

    def engage(self, student: Student, module_id: str):
        """ engages a student with a supervisor """
        if not self.is_free():
            raise ValueError("can't add student to supervisor if supervisor is not free")
        self.assigned_students.append((module_id, student))

    def is_free(self):
        """ :returns whether the supervisor is free or has reached max students """
        return len(self.assigned_students) < self.max_students  # limit the supervisor capacity to max_students

    @classmethod
    def from_list(cls, l: list):
        """ :returns an initialised object from the list

        a list has:
        Firstname,Lastname,Prefered_studentNO,Module1,Module2,Supervisor_ID
        """
        # add non-null modules
        modules = []
        if l[3] != '':
            modules.append(l[3])
        if l[4] != '':
            modules.append(l[4])

        return cls(
            first_name=l[0],
            last_name=l[1],
            max_students=int(l[2]),
            modules=tuple(modules),
            id=l[5],
            assigned_students=[]
        )

    def __str__(self):
        return f"Supervisor({self.id})"
