# tests/test_accounts.py
import sys
import os
# import pytest

# Add the root directory to sys.path so Python can find accounts.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import accounts
from accounts import Student
# def test_prereqs_taken_all_met():
    
#     accounts.course_prereqs['CS1000'] = ['CS2000', 'CS3000']
#     accounts.courses_taken.update(['CS2000', 'CS3000'])

#     assert accounts.prereqs_taken('CS1000') == True

def test_all_major_minor_combinations():
    majors_list = ["CS", "CEG"]
    minors_list = ["PHY", "MTH"]

    major_combos = [[]]
    minor_combos = [[]]

    for i in range(len(majors_list)):
        major_combos.append([majors_list[i]])
    for i in range(len(minors_list)):
        minor_combos.append([minors_list[i]])

    for i in range(len(majors_list)):
        for j in range(i+1, len(majors_list)):
            major_combos.append([majors_list[i], majors_list[j]])

    for i in range(len(minors_list)):
        for j in range(i+1, len(minors_list)):
            minor_combos.append([minors_list[i], minors_list[j]])

    for major_set in major_combos:
        for minor_set in minor_combos:
            student = Student("Test", "testuser", "Password123!")
            for m in major_set:
                assert student.add_major(m) == True
            for m in minor_set:
                assert student.add_minor(m) == True
            assert student.majors == major_set
            assert student.minors == minor_set

    print("All major/minor combinations completed.")

def test_student_approve_proposed_schedule():
    student = Student("Test", "testuser", "Password123!")

    assert student.approve_proposed_schedule() == "You have no proposed schedule to approve."

    student.proposed_schedule = [
        ["CS1180", "MTH2300"],
        ["CEG2170", "ENG1100"]
    ]

    assert student.approve_proposed_schedule() == True
    assert student.schedule == student.proposed_schedule
    assert student.sched_student_approved == True

def test_student_reject_proposed_schedule():
    student = Student("Test", "testuser1", "Password123!")

    student.proposed_schedule = [
        ["CS1180", "MTH2300"],
        ["CEG2170", "ENG1100"]
    ]

    assert student.sched_student_approved == False
    assert student.schedule == []

def test_student_semesters_to_graduate_zero():
    student = Student("Test", "testuser", "Password123!")
    student.semesters_to_graduate = 0
    student.new_num_semesters = 0

    assert student.semesters_to_graduate == 0
    assert student.new_num_semesters == 0
    # Tested on Render and it worked

def test_student_semesters_to_graduate_one():
    student = Student("Test", "testuser", "Password123!")
    student.semesters_to_graduate = 1
    student.new_num_semesters = 1

    assert student.semesters_to_graduate == 1
    assert student.new_num_semesters == 1
    # Tested on Render and it worked

def test_student_semesters_to_graduate_twentyfour():
    student = Student("Test", "testuser", "Password123!")
    student.semesters_to_graduate = 24
    student.new_num_semesters = 24

    assert student.semesters_to_graduate == 24
    assert student.new_num_semesters == 24
    # Tested on Render and it worked

def test_student_semesters_to_graduate_nonnumeric():
    student = Student("Test", "testuser", "Password123!")
    student.semesters_to_graduate = 'a'
    student.new_num_semesters = 'a'

    assert student.semesters_to_graduate == 'a'
    assert student.new_num_semesters == 'a'
    # Tested on Render and it caused internal server error

# Scheduling algorithm: Test schedule generation with 1 major and 2 minors: this would be hard to do with code here but it worked on website
# Scheduling algorithm: Test schedule generation without input from student on number of semesters to graduate in: again hard to test here but it properly caused a popup requesting a number be entered


def test_create_student_account():
    admin = accounts.Admin("admin", "adminadmin", "Adminadmin123$")
    name = "Bob Marley"
    username = "bmarley1"
    password = "Password123$"

    assert admin.create_student(name,username, password) == True

def test_create_faculty_account():
    admin = accounts.Admin("admin", "adminadmin", "Adminadmin123$")
    name = "Mr. Faculty"
    username = "mfaculty"
    password = "Password123$"

    assert admin.create_faculty(name,username, password) == True

def test_create_admin_account():
    admin = accounts.Admin("admin", "adminadmin", "Adminadmin123$")
    name = "Alan Admin"
    username = "aadmin12"
    password = "Password123$"

    assert admin.create_admin(name,username, password) == True