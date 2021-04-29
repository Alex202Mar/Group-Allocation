import csv

from gale_shapley import gale_shapley
from student import Student
from supervisor import Supervisor


def _parse_cls(path, cls):
    """ :returns a list of objects, parsed from the csv file in path """
    parsed_objects = []
    with open(path) as f:
        csv_reader = csv.reader(f)
        next(csv_reader)  # skip header
        for row in csv_reader:
            parsed_objects.append(cls.from_list(row))
    return parsed_objects


def parse_students(path):
    """ :returns a list of students parsed from the csv in path """
    return _parse_cls(path, Student)


def parse_supervisors(path):
    """ :returns a list of supervisors parsed from the csv in path """
    return _parse_cls(path, Supervisor)


def main():
    students = parse_students('students.csv')
    supervisors = parse_supervisors('supervisors.csv')

    # change module_id preferences for supervisor preferences to which students want to propose to
    for student in students:
        student.load_preferences_supervisors(supervisors)

    # run Gale Shapley
    gale_shapley(students)

    # print output to console
    for student in students:
        print(f"Student {student.id} will be learning {student.assigned_module_id} with {student.assigned_supervisor} and is {student.happiness()}")

    # save output to file
    with open('output.csv', 'w', newline='') as file:
        writer = csv.writer(file, escapechar='/', quoting=csv.QUOTE_NONE)
        writer.writerows([[student.id, student.assigned_module_id, student.assigned_supervisor.id] for student in students])


if __name__ == "__main__":
    main()
