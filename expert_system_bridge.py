import mysql.connector
from clips import Environment

db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="expert_system"
)

db_cursor = db_connection.cursor()

env = Environment()

env.load("rules.clp")

def load_courses_into_clips():
    db_cursor.execute("SELECT id, name, prerequisites FROM courses")
    courses = db_cursor.fetchall()
    for course in courses:
        course_id, course_name, prerequisites = course
        prerequisites_list = [p.strip().upper() for p in prerequisites.split(',')] if prerequisites else []
        prerequisites_str = " ".join([f'"{p}"' for p in prerequisites_list])
        prerequisites_fact = f'(course (id "{course_id.upper()}") (name "{course_name}") (prerequisites {prerequisites_str}))'
        # print(f"Loaded course fact: {prerequisites_fact}")
        env.assert_string(prerequisites_fact)

def load_students_into_clips():
    db_cursor.execute("SELECT id, name, completed_courses FROM students")
    students = db_cursor.fetchall()
    for student in students:
        student_id, student_name, completed_courses = student
        completed_courses_list = [c.strip().upper() for c in completed_courses.split(',')] if completed_courses else []
        completed_courses_str = " ".join([f'"{c}"' for c in completed_courses_list])
        completed_courses_fact = f'(student (id "{student_id}") (name "{student_name}") (completedCourses {completed_courses_str}))'
        # print(f"Loaded student fact: {completed_courses_fact}")
        env.assert_string(completed_courses_fact)

load_courses_into_clips()
load_students_into_clips()


# for fact in env.facts():
#     print(fact)

# Run inference engine
env.run()

db_cursor.close()
db_connection.close()
