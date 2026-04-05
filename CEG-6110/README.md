# CEG-6110

This is the main repository containing all source code belonging to The Magic School Kids team for CEG-6110.

## Team Members

* Shane Martin
* Josiah Schmitz
* Luke Kaufman

## Project Description

This is a course scheduling program that uses the Wright State University course catalog to generate schedules
for a student depending on their degree choices.

---
Users can be one of three account types with different main pages and functionalities on login:
* Student - can add up to two majors and minors each and view and approve proposed schedules
* Faculty - can approve majors and minors and approve or reject proposed schedules
* Admin - can create and remove accounts of all types and assign students to faculty

---
The course scheduler generates and displays possible schedules for the student,
dependent on their majors and minors and the number of semesters they hope to graduate in.
If a schedule cannot be generated in the given number of semesters,
the scheduler will suggest a schedule that allows the student to graduate in as few semesters as possible.
