# tests/test_login.py
import sys
import os

# Add the root directory to sys.path so Python can find login.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import scheduling, accounts, random

# NOTE FOR ALL TESTS: Each test checks if the return type is str 
# (an error message) if the criteria are not met, or if the method returns true.


def test_prereqs_taken_all_met():
    scheduling.build_dicts()
    scheduling.courses['CS1000'].preqreqs = ['CS2000', 'CS3000']
    scheduling.courses_taken.update(['CS2000', 'CS3000'])

    assert scheduling.prereqs_taken('CS1000') == True
    
def test_prerequisite_lists_for_course_are_built():
    scheduling.build_dicts()
    courses = scheduling.courses
    check = False
    for i in range(5):
        rand = random.randrange(len(courses))
        value = list(courses.values())[rand]
        if value.prereqs == '' or not value.prereqs:
            check = True
    assert check == True


def test_generate_CS_Major():
    scheduling.build_dicts()
    catalog = scheduling.course_catalog
    student1 = accounts.Student("Shane Martin", "martin12", "Password123$")
    student1.add_major("CS Major")
    courses = scheduling.courses
    ret = scheduling.generate_schedule(student1)
    success = ret[0]
    sched = ret[2]

    assert (sched and success == True) == True 

def test_generate_CEG_Major():
    scheduling.build_dicts()
    catalog = scheduling.course_catalog
    student1 = accounts.Student("Shane Martin", "martin12", "Password123$")
    student1.add_major("CEG Major")
    courses = scheduling.courses
    ret = scheduling.generate_schedule(student1)
    success = ret[0]
    sched = ret[2]

    assert (sched and success == True) == True 

def test_generate_CEG_Major_1minor():
    scheduling.build_dicts()
    catalog = scheduling.course_catalog
    student1 = accounts.Student("Shane Martin", "martin12", "Password123$")
    student1.add_major("CEG Major")
    student1.add_major("Math Minor")
    courses = scheduling.courses
    ret = scheduling.generate_schedule(student1)
    success = ret[0]
    sched = ret[2]

    assert (sched and success == True) == True 

def test_generate_CEG_Major_other_minor():
    scheduling.build_dicts()
    catalog = scheduling.course_catalog
    student1 = accounts.Student("Shane Martin", "martin12", "Password123$")
    student1.add_major("CEG Major")
    student1.add_major("Physics Minor")
    courses = scheduling.courses
    ret = scheduling.generate_schedule(student1)
    success = ret[0]
    sched = ret[2]

    assert (sched and success == True) == True

def test_generate_CEG_Major_both_minors():
    scheduling.build_dicts()
    catalog = scheduling.course_catalog
    student1 = accounts.Student("Shane Martin", "martin12", "Password123$")
    student1.add_major("CEG Major")
    student1.add_major("Math Minor")
    student1.add_major("Physics Minor")
    courses = scheduling.courses
    ret = scheduling.generate_schedule(student1)
    success = ret[0]
    sched = ret[2]

    assert (sched and success == True) == True


def test_generate_CS_Major_1minor():
    scheduling.build_dicts()
    catalog = scheduling.course_catalog
    student1 = accounts.Student("Shane Martin", "martin12", "Password123$")
    student1.add_major("CS Major")
    student1.add_major("Math Minor")
    courses = scheduling.courses
    ret = scheduling.generate_schedule(student1)
    success = ret[0]
    sched = ret[2]

    assert (sched and success == True) == True 

def test_generate_CS_Major_other_minor():
    scheduling.build_dicts()
    catalog = scheduling.course_catalog
    student1 = accounts.Student("Shane Martin", "martin12", "Password123$")
    student1.add_major("CS Major")
    student1.add_major("Physics Minor")
    courses = scheduling.courses
    ret = scheduling.generate_schedule(student1)
    success = ret[0]
    sched = ret[2]

    assert (sched and success == True) == True

def test_generate_CS_Major_both_minors():
    scheduling.build_dicts()
    catalog = scheduling.course_catalog
    student1 = accounts.Student("Shane Martin", "martin12", "Password123$")
    student1.add_major("CS Major")
    student1.add_major("Math Minor")
    student1.add_major("Physics Minor")
    courses = scheduling.courses
    ret = scheduling.generate_schedule(student1)
    success = ret[0]
    sched = ret[2]

    assert (sched and success == True) == True


def test_generate_both_majors():
    scheduling.build_dicts()
    catalog = scheduling.course_catalog
    student1 = accounts.Student("Shane Martin", "martin12", "Password123$")
    student1.add_major("CS Major")
    student1.add_major("CEG Major")
    courses = scheduling.courses
    ret = scheduling.generate_schedule(student1)
    success = ret[0]
    sched = ret[2]

    assert (sched and success == True) == True

def test_generate_both_majors_1minor():
    scheduling.build_dicts()
    catalog = scheduling.course_catalog
    student1 = accounts.Student("Shane Martin", "martin12", "Password123$")
    student1.add_major("CS Major")
    student1.add_major("CEG Major")
    student1.add_minor("Math Minor")
    courses = scheduling.courses
    ret = scheduling.generate_schedule(student1)
    success = ret[0]
    sched = ret[2]

    assert (sched and success == True) == True

def test_generate_both_majors_other_minor():
    scheduling.build_dicts()
    catalog = scheduling.course_catalog
    student1 = accounts.Student("Shane Martin", "martin12", "Password123$")
    student1.add_major("CS Major")
    student1.add_major("CEG Major")
    student1.add_minor("Physics Minor")
    courses = scheduling.courses
    ret = scheduling.generate_schedule(student1)
    success = ret[0]
    sched = ret[2]

    assert (sched and success == True) == True

def test_generate_both_majors_both_minors():
    scheduling.build_dicts()
    catalog = scheduling.course_catalog
    student1 = accounts.Student("Shane Martin", "martin12", "Password123$")
    student1.add_major("CS Major")
    student1.add_major("CEG Major")
    student1.add_minor("Math Minor")
    student1.add_minor("Physics Minor")
    courses = scheduling.courses
    ret = scheduling.generate_schedule(student1)
    success = ret[0]
    sched = ret[2]

    assert (sched and success == True) == True

def test_generate_with_semesters_input_from_student():
    scheduling.build_dicts()
    catalog = scheduling.course_catalog
    student1 = accounts.Student("Shane Martin", "martin12", "Password123$")
    student1.add_major("CS Major")
    student1.add_minor("Physics Minor")
    student1.num_semesters = 6
    courses = scheduling.courses
    ret = scheduling.generate_schedule(student1)
    success = ret[0]
    sched = ret[2]

    assert (sched and success == True) == True

def test_generate_with_semesters_input_24_from_student():
    scheduling.build_dicts()
    catalog = scheduling.course_catalog
    student1 = accounts.Student("Shane Martin", "martin12", "Password123$")
    student1.add_major("CS Major")
    student1.add_minor("Physics Minor")
    student1.num_semesters = 24
    courses = scheduling.courses
    ret = scheduling.generate_schedule(student1)
    success = ret[0]
    sched = ret[2]

    assert (sched and success == True) == True
