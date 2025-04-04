import copy
import time
from enum import Enum
from dataclasses import dataclass

@dataclass
class Node:
    student_info: dict
    calendar: dict

class Student(Enum):
    STUDENT1 = 0
    STUDENT2 = 1
    STUDENT3 = 2
    STUDENT4 = 3

class Exam(Enum):
    EXAM1 = 0
    EXAM2 = 1
    EXAM3 = 2
    EXAM4 = 3
    EXAM5 = 4
    EXAM6 = 5
    EXAM7 = 6

    def __lt__(self, other):
        return self.value < other.value


class Day(Enum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2

MAX_EXAMS_PER_STUDENT = 3
MAX_EXAMS_PER_DAY = len(Student)

def initial_node():
    student_info = {student: [] for student in Student}
    calendar = {day: [] for day in Day}
    return Node(student_info, calendar)

def is_complete(node):
    return all(len(exams) == MAX_EXAMS_PER_STUDENT for exams in node.student_info.values())

def select_unassigned_variable(node):
    for student in Student:
        if len(node.student_info[student]) < MAX_EXAMS_PER_STUDENT:
            return student
    return None

def order_domain_values(node, student):
    assigned_exams = {exam for exam, _ in node.student_info[student]}
    available_exams = [exam for exam in Exam if exam not in assigned_exams]
    return sorted(available_exams)

def assign(node, student, exam, day):
    new_node = copy.deepcopy(node)
    new_node.student_info[student].append((exam, day))
    new_node.calendar[day].append(exam)
    return new_node

def is_consistent(node):
    for day in Day:
        if len(set(node.calendar[day])) > MAX_EXAMS_PER_DAY:
            return False
    return True

def backtracking(node):
    if is_complete(node):
        return node
    
    student = select_unassigned_variable(node)
    if not student:
        return None
    
    for exam in order_domain_values(node, student):
        for day in Day:
            new_node = assign(node, student, exam, day)
            if is_consistent(new_node):
                result = backtracking(new_node)
                if result:
                    return result
    return None

def print_solution(node):
    if not node:
        print("No solution found.")
        return
    print("Solution found:")
    for student, exams in node.student_info.items():
        print(f"{student.name}:")
        for exam, day in exams:
            print(f"  {exam.name} on {day.name}")
        print()

# Ejecutar búsqueda con backtracking
start_time = time.time()
initial = initial_node()
solution = backtracking(initial)
end_time = time.time()

print_solution(solution)
print(f"Execution time: {end_time - start_time:.5f} seconds")
