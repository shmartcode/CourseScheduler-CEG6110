# Course Scheduler

This program’s purpose is to allow students to generate schedules that fit their degree program and preferred timeframe in a quick and efficient manner.

## Description

The Course Scheduler is a group project for Wright States Intro to Software Engineering course. For my (Shane Martin) individual contributions and work please see bewlo. The program generates class schedules for students based on their degree programs and the timeframe they want to graduate in. If a schedule cannot be generated in the given timeframe (number of semesters), the scheduler will suggest a schedule that allows the student to graduate in as few semesters as possible. It runs on a website (ceg-6110-2.onrender.com) that is hosted using the free sercices of Render. It is completely self-contained and contains features for both administrative and student accounts. This base version of the program was enacted for use with 2 majors and 2 minors. Each of the major/minor requirements were built manually into CSV files. 

## Try the website!

* You can try the program yourself by visiting "ceg-6110-2.onrender.com". Please be patient as Render's free web services "spin down after 15 minutes of inactivity, and waking them can take 30 seconds or more". This usually translates to a 2-5 minute loading time.
* The sample accounts to log in with are as follow:
*   "student1" : "Password123$"
*   "adminadmin" : "Adminadmin123$"


## Authors

Contributors names

* Luke Kaufman
* Josiah Schmitz
* Shane Martin

## Version History

1.0.0
    * Initial Release

## Individual Contributions of Shane Martin
My primary focus was on RBAC and the algorithm. Most of my work was within the accounts.py, login.py, and scheduling.py files.
* accounts.py in its entirety.
* login.py in its entirety.
* schuedling.py, fully coded, generate_schedule(student), build_chain(student), sort_prereqs_chain(), calc_total_credit(), get_prereqs_as_list(course), and build_empty_schedule(num_sems)
* scheduling.py, debugged / reworked, schedule_course(course)
* test_scheduling.py, tiny bit of work here completing  two functions: test_prereqs_taken_all_met() and test_prerequisite_lists_for_course_are_built()
* "...Simplified.csv", all simplified CVS built manually from the regular equavilents (CompEng.csv -> CompEngSimlified.csv). The simplified versions take the first course in any given or / multi-or statement.

## Additional Notes:
* Some aspects of this project were simplified in order to meet timelines of the course, such as the simplified.csvs to layout the basic course requirements to attain a degree in the chosen major/minor.
* Faculty accounts and admin accounts were also not fully implemented as the crux of the project was to demonstrate an algorithm that could easily and quickly assemble a course schedule given a graduation estimation and degree outline(s).
