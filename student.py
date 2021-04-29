from dataclasses import dataclass, field
from queue import Queue

from typing import TYPE_CHECKING, List, Tuple, Union

if TYPE_CHECKING:
    from supervisor import Supervisor


@dataclass
class Student:
    first_name: str
    last_name: str
    attendance_score: float
    grade_score: float
    total_score: float
    preferences: Queue[str]
    preferences_supervisors: Queue[Tuple[str, 'Supervisor']]
    id: str
    priorities_in: field(default_factory=tuple)

    assigned_supervisor: Union['Supervisor', None] = None
    assigned_module_id: Union[str, None] = None

    def __post_init__(self):
        # save original preferences
        self.original_preferences = [item for item in self.preferences.queue]

    def happiness(self):
        """ :returns a happiness representation """
        if self.assigned_module_id is None:
            return "😭😭"  # no assigned module
        try:
            index = self.original_preferences.index(self.assigned_module_id)
            return "😃" * (len(self.original_preferences) - index)  # the happier, the best the preference
        except IndexError:
            return "😭"  # assigned module was not in preferences

    def is_stable(self):
        """ :returns whether this student has found a stable situation """
        return not (self.is_free() and self.has_preference())

    def engage(self, supervisor: 'Supervisor', module_id: str):
        """ engages a student with a supervisor """
        self.assigned_supervisor = supervisor
        self.assigned_module_id = module_id

    def un_engage(self):
        """ un-engages a student with a supervisor """
        self.assigned_supervisor = None
        self.assigned_module_id = None

    def load_preferences_supervisors(self, supervisors: List['Supervisor']):
        """ loads to the preference queue the supervisors in order (of the preferred module) """
        while not self.preferences.empty():
            module_id = self.preferences.get()
            for supervisor in supervisors:
                if supervisor.teaches(module_id):
                    self.preferences_supervisors.put((module_id, supervisor))

    def is_free(self):
        """ :returns whether the student is free or has already a supervisor """
        return self.assigned_module_id is None or self.assigned_supervisor is None

    def has_preference(self):
        """ :returns whether the student still has a preferred module to try """
        return not self.preferences_supervisors.empty()

    @classmethod
    def from_list(cls, l: list):
        """ :returns an initialised object from the list

        a list has:
        First Name,Last Name,Attendance,Grade Average,Rating,Preferred_Module,Backup1,Backup2,StudentID,Priority
        """

        # add the preferences in order to the preferences queue
        preferences = Queue()
        preferences.put(l[5])
        preferences.put(l[6])
        preferences.put(l[7])

        return cls(
            first_name=l[0],
            last_name=l[1],
            attendance_score=float(l[2])/100,
            grade_score=float(l[3])/100,
            total_score=float(l[4]),
            preferences=preferences,
            preferences_supervisors=Queue(),
            id=l[8],
            priorities_in=(l[9]) if l[9] != '' else tuple()
        )

