# Imports:
import copy
import accounts
import csv
import struct
from pprint import pprint

# Variables:
course_catalog = {}     # {major/minor : set(courses)}. This dictionary is accessed with key 'major/minor' and 
                        # gives the value which is the 'set' of all courses you must take for completion of said major/minor
courses = {}            # {course code : course Object} dict built Classes.csv. will replace courses_prereqs.
courses_taken = set()   # set of courses that have been taken (ie are on the schedule already)
proposed_schedule = []  # list of sets. each set loosely portrays a semester of courses (length of set may change)
prereq_chain = []       # list of lists. used to store all courses to be taken in order of the length of their prerequisite chains.
num_sems = 0            # the number of semesters the algorithm will use to create the proposed_schedule. 
                        # initially set based on student.num_semesters but may be changed based on prereq chains or total credits to take
credits_per_sem = 15     # how many credits can be scheduled per semester. default is 15 (max is 20).
credits_required = 0    # total number of credits required to fullfill all majors/minors course requirements

# CHANGE LOG: Changes made to prevent duplicate course scheduling (mostly for reference for Shane):
# 1. generate_schedule() now calls scheduling_init() at the start to reset globals.
# 2. After scheduling a course, it (and its coreqs) get put in courses_taken so later semesters won't
#    attempt to schedule them again.
# 3. When removing scheduled items from prereq_chain we remove all occurrences to keep chains from retaining scheduled courses.

# Support Functions:
### 1. prereqs_taken(course) : looks up if the prequisites of 'course' have been satisified (should be in course_taken). returns true/false
### 2. schedule_course(course) : adds a course to the 'proposed_schedule' list[set()]. must account for sets being full and also that prereqs for said course are not being taken in same semester.
###         once added 'course' must also be removed from the relevant set/sets within 'prereq_chain'. return true/false
### 3. sort_prereqs_chain : sorts the 'prereq_chain' list in order of longest prerequisite chain. 
###         needed so we can resort as courses are taken, ensuring that we always meet the semesters required to complete the longest chain of prerequisites
### 4. build_dicts : reference CSV files to build course_catalog dict and course prereqs dict
### 5. build_chain : reference the course catalog and course prereqs dicts for each major and minor and add the courses to the 'prereq_chain'

class Course:
    def __init__(self, code, title, credits:int, prereqs:list, coreqs:list):
        self.code = code    # the course code. ie PHY2400
        self.title = title  # the title of the course
        self.credits = credits  # number of credits the course is worth
        self.prereqs = prereqs  # a set of the courses prereqs or "" if none
        self.coreqs = coreqs    # a set of the courses coreqs or "" if none
    def __str__(self):
        return f"{self.code}: {self.title} ({self.credits} cr)."

def prereqs_taken(course):
    """Takes in a course and looks up if the prequisites of 'course' have been satisified (should be in courses_taken). returns true/false"""
    prereqs = courses[course].prereqs # gets prereq list for given course
    if prereqs == '':   # if we dont have any prereqs then the course can be taken so return true
        return True
    else:
        for preq in prereqs: # iterate over each prereq of course
            if preq not in courses_taken: # if a prereq hasn't been taken, return false
                return False
    return True # if all prereqs have been taken, return true


def schedule_course(course):
    """Adds a course to the 'proposed_schedule' by its code. must account for sets being full and also that prereqs for said course are not being taken in same semester.
    Once added 'course' must also be removed from the relevant set/sets within 'prereq_chain'. Returns (scheduled, reschedule)"""
    global proposed_schedule
    global credits_per_sem
    global prereq_chain
    global courses_taken

    prereqs = courses[course].prereqs
    coreqs = courses[course].coreqs
    scheduled = False
    found_reqs = []
    found_all = 0
    fullsems = 0
    reschedule = False
     
    for semester in proposed_schedule:
        sem_credits = 0     # variable so we can track total credits in any semester and check against max credits per semeester
        
        for c in semester:  # loop to calc the current total of credits in this semester
            sem_credits += courses[c].credits
        
        if len(prereqs) == 0 or len(prereqs) == found_all:     # we do not have any prereqs to find or we have found them all
            if len(coreqs) != 0:
                credit_space_needed = courses[course].credits
                for co in coreqs:       # loop through coreq courses to tally credit total between course and its coreqs
                    credit_space_needed += courses[co].credits
                                 
                if sem_credits <= credits_per_sem and (sem_credits + credit_space_needed) <= credits_per_sem: # check if semester has room for the credits we want to schedule
                    semester.append(course)
                    for co in coreqs:
                        if co not in semester and co not in courses_taken:
                            semester.append(co)
                    scheduled = True
                    break
            elif sem_credits <= credits_per_sem and (sem_credits + courses[course].credits) <= credits_per_sem: # check if semester has room for the credits we want to schedule
                semester.append(course)
                scheduled = True
                break
            else:
                fullsems += 1
        else:
            for p in prereqs:     # loop through all prereqs
                if p in semester:   # if we find one in this semester
                    found_reqs.append(p)   # add it to the found set
                    found_all += 1
    if scheduled:
        # CHANGE: mark scheduled course and its coreqs as taken so they aren't scheduled again later.
        # This is critical to prevent duplicate scheduling across multiple iterations.
        courses_taken.add(course)
        if isinstance(coreqs, list):
            for co in coreqs:
                courses_taken.add(co)
        # CHANGE: remove scheduled items (course + coreqs) from prereq_chain safely so they are not considered again.
        to_remove = [course]
        if isinstance(coreqs, list):
            to_remove.extend(coreqs)
        for rem_course in to_remove:
            for chain in prereq_chain[:]:
                while rem_course in chain:
                    chain.remove(rem_course)
                if chain == []:
                    prereq_chain.remove(chain)
    else:
        # print(f"fullsems: {fullsems}")
        if credits_per_sem < 20:
            credits_per_sem += 1
        else:
            # print("All sems full, adding 1 more") # TESTING
            global num_sems
            num_sems += 1
            emptySemester = []
            proposed_schedule.append(emptySemester)
        reschedule = True


    return scheduled, reschedule # successfully scheduled course


def build_chain(student):
    """Build the preqchain based on the students majors/minors. For each major/minor the student is taking go through its entire catalog, get the corresponding preqs
    set from course.prereqs and add it to the prereqs chain"""
    global prereq_chain
    prereq_chain = []
    build_from = student.majors[:] # create 1 set to include all majors/minors
    for item in student.minors:
        if item not in build_from:
            build_from.append(item)
            
    for m in build_from:        # for each major/minor in the set
        catalog = course_catalog[m] # find its course catalog
        for course in catalog:      # then for each course in the major/minors catalog
            if course.endswith("L") or course.endswith("R"): # skip coreq lab and recital courses. they will be handled in schedule_course()
                continue 
            else:
                c = get_prereqs_as_list(course)    # turn the current course into a list 
                prereq_chain.append(c)

def get_prereqs_as_list(course):
    """Takes in a course code and compiles that courses entire prerequisite chain as a list and returns it"""
    stack = [course]    # stack, a loop driving list. this is a list! i only call it stack because it functions similarly
    result = []         # the full list of prereqs to be returned
    visited = set() 

    while stack:    # while we have courses in stack we must get all of their prereqs
        current = stack.pop(0)      # need to pop from the front of the list
        if current in visited:
            result.remove(current)          # if we find a prereq a second time it means there is a second course that requires it at a lower level
                                            # so remove if from its current spot and let it get added back in the new spot lower down the chain
        visited.add(current)    # add the current course to the visited list to show it has been handled
        result.append(current)  # add the current course to result list

        if courses[current].prereqs != "":  # if the course has additional prereqs put them on the stack of courses we have to check for additional prereqs
            # print(f"{current}preqs: {courses[current].prereqs}")
            stack.extend(courses[current].prereqs)
    result.reverse()    # reverse the prereqs so that the higher level courses are at the end
    return result


def sort_prereqs_chain():
    """Sorts the 'prereq_chain' list in order of longest prerequisite chain first. Inside the each chain it is sorted by course level. Is neeeded so we can resort as courses are taken, ensuring that we always meet the semesters required to complete the longest chain of prerequisites"""
    global prereq_chain
    prereq_chain.sort(reverse = True, key = lambda sublist : len(sublist))

def calc_total_credits():
    """Goes through the prereq chain and counts total number of courses to determine the total credits the student will take to complete their majors/minors.
    Returns the total number of credits"""
    # must account for courses appearing in multiple prereq chains()
    counted = set()
    total = 0
    for chain in prereq_chain:
        for course in chain:
            if course not in counted:   # if we havent counted the course before the increase total count
                total += courses[course].credits
                counted.add(course)
    return total

def build_dicts():
    """Calls the build_course() and build_catalog() functions"""
    # Notes: course_catalog {major/minor : set(courses)} and courses {course code : course Object}   (see above for details)
    build_courses()
    build_catalog()

def build_courses():
    """Read CSV files to build courses dict"""
    # Notes: course{course code: course Object}   (see above for details)
    #CSV file layout
    # Code,name,credits,Prereq's,coreq's,availability
    #  0    1      2      3        4        5
    # CEG2171,C++ Programming for Scientists and Engineers,4,CEG2170,CEG2171L,availability
    
    with open('Classes.csv', newline='') as csvfile:
        csvFile = csv.reader(csvfile, delimiter=',')
        next(csvFile) #Skips header
        for row in csvFile:
            if row[3] == '':    # row3 is prereqs. if its empty set r3 to ''
                r3 = ''
            else:
                r3 = row[3].split(" and ") # if there are prereqs split them on "and"
            if row[4] == '':    # row4 is coreqs
                r4 = ''
            else:
                r4 = row[4].split(" and ")  # if there are coreqs split them on "and"
            newCourse = Course(row[0], row[1], int(row[2]), r3, r4)
            courses[row[0]] = newCourse     # add the course object to the dict by its code
    # end build_courses


def build_catalog():
    # """Read CSV files to build course_catalog dict """
    # Notes: course_catalog {major/minor : set(courses)}
    math_courses = []
    computer_science_courses = []
    computer_engineering_courses = []
    physics_courses = []
    # Building Math Minor
    with open('MathSimplified.csv', newline='') as csvfile:
        csvFile = csv.reader(csvfile, delimiter=' ')
        for row in csvFile:
            # print(row[0])
            math_courses.append(row[0])
    # Building Physics minor
    with open('PhysicsSimplified.csv', newline='') as csvfile:
        csvFile = csv.reader(csvfile, delimiter=' ')
        for row in csvFile:
            physics_courses.append(row[0])
    # Building Computer Engineering Major
    with open('CompEngSimplified.csv', newline='') as csvfile:
        csvFile = csv.reader(csvfile, delimiter=' ')
        for row in csvFile:
            computer_engineering_courses.append(row[0])
    # Building Computer Science Major
        with open('CompSciSimplified.csv', newline='') as csvfile:
            csvFile = csv.reader(csvfile, delimiter=' ')
            for row in csvFile:
                computer_science_courses.append(row[0])
    # Add all majors/minors to course_Catalog
    course_catalog["Math Minor"] = math_courses
    course_catalog["Physics Minor"] =physics_courses
    course_catalog["CEG Major"] = computer_engineering_courses
    course_catalog["CS Major"] = computer_science_courses
    # end build_catalog

def generate_schedule(student):
    """Takes in a student object and builds that students schedule. Sets message and sem_message depending on the results of the algo.
    Returns True/False, list of messages, and the propposed schedule"""
    
    # CHANGE: Initialize / reset global variables to avoid stale state from previous runs
    scheduling_init()

    messages = []             # will be part of return. will contain strings of things such as error messages, success messages, and/or increasing credits_per_sem or num_sems
    student_sems = 0            # the number of semesters the algorithm will use to create the proposed_schedule. 
                            # initially set based on student.num_semesters but may be changed based on prereq chains or total credits to take
    global num_sems
    global credits_per_sem     # how many credits can be scheduled per semester. default is 15 (max 20).
    global prereq_chain
    credits_required = 0    # total number of credits required to fullfill all majors/minors course requirements
    success = True          # value to be returned by function

    # set some variables
    build_chain(student)
    num_sems = student.num_semesters
    student_sems = student.num_semesters     # set both equal to the requested number of semesters by the student. student_sems will not be changed.
    credits_required = calc_total_credits()
       
    sort_prereqs_chain()    # call sort on prereqs chain
    longest = len(prereq_chain[0])  # get the length of the longest prereq chain which should be the first chain if sort is proper

    changed = False     # tracker variable to for setting the semester message
    # if longest > num_sems:  # check if the requested number of semesters is less than the longest prereq chain. ie we need more semesters to complete it
    #     num_sems = longest
    #     changed = True
    # while (credits_required / credits_per_sem) > num_sems :  # loop and increase number of semesters while the total credits doesnt fit into num_sems
    #         if credits_per_sem < 20:
    #             credits_per_sem += 1    # add 1 more credit to the toal per sem
    #         else:
    #             num_sems += 1
    #             changed = True

    build_empty_schedule(num_sems)

    loop = 0
    # While loop to go through all the courses the student must take (the prereq chain) and add each one to the proposed_schedule
    while prereq_chain:
        loopm = []      # messages held during while loop
        # loop += 1       # TESTING
        # if loop > 50:   # TESTING
        #     break       # TESTING
        # # chain_length = sum(len(x) for x in prereq_chain)       # TESTING temp var to track length of chains for testing
        
        course_to_schedule = prereq_chain[0][0] # grab the first course from the first prereq chain list
        
        # print(f"\nchain len: {chain_length}", end = ' ') # TESTING
        # print(f"numsem: {num_sems}", end = ' ') # TESTING
        # print(f"course to schedul: {course_to_schedule}") # TESTING
        # print(f"sched:{proposed_schedule}") # TESTING

        if prereqs_taken(course_to_schedule):   # check if the courses prereqs have all been taken
            scheduled, reschedule = schedule_course(course_to_schedule)
            if scheduled:     # try to schedule the course
                courses_taken.add(course_to_schedule)
                sort_prereqs_chain()    # sort the chain again so its ready for the next scheduling round.
            elif reschedule:
                continue
            else:
                sched_message = f"Could not schedule: {course_to_schedule} "   # set a message. helpful in case we need to print for debugging
                preqlist = courses[course_to_schedule].prereqs
                # print(f"{course_to_schedule} prereq list({len(preqlist)}): {preqlist}")   # TESTING
                # count = 0   # TESTING
                # for s in proposed_schedule:   # TESTING
                #     for l in s:   # TESTING
                #         count += 1   # TESTING
                # print(f"sched({count}):{proposed_schedule}") # TESTING
                # messages.append(sched_message)    # REPLACED BY loopm. add message to return list
                loopm.append(sched_message)    # add message to return list
                success = False
        else:
            prereq_mess = f"Prereqs not met for: {course_to_schedule} "
            loopm.append(prereq_mess)
            success = False
            break
        # print(f"mess: {loopm}")    # temp line for testing
    
    clean_message = clean_up()
    
    if student_sems != num_sems:
        if clean_message is not None:
            messages.append(clean_message)
            student.new_num_sems = num_sems # sets student var new_num_sems in case we need it for message display later
        # check if we had to increase the number of semesters and add a message to the return message list accordingly
        else:
            messages.append(f"Number of semesters automatically increased to {num_sems}.")
            student.new_num_sems = num_sems # sets student var new_num_sems in case we need it for message display later
    else:
        messages.append("Requested number of semesters accepted.")

    messages.append(f"Maximum credits per semester set to {credits_per_sem}.")  # add messge to return message list for how many semesters they will take per semester

    if success: # since we completed the while loop the prposed schedule should be generated so set it in the student accoun
        sched_return = copy.deepcopy(proposed_schedule)    # using a copy just to be safe
    else:
        sched_return = []

    messages.extend(loopm)  # adds all messages created inside the while loop to the list of other messages. extend adds them invidually (whereas append would add the list object)
    return (success, messages, sched_return)


def build_empty_schedule(num_sems):
    """Creates the empty propose_schedule list with n number of empty sets based on the determined number of semesters required"""
    global proposed_schedule
    for x in range(num_sems):
        emptySemester = []
        proposed_schedule.append(emptySemester)

def clean_up():
    
    """Clears empty semesters from extra long schedules"""
    global proposed_schedule
    global num_sems
    cleaned_schedule = []
    new_sem_count = 0
    cleanup_needed = False
    for semester in proposed_schedule:
        if semester != []:
            cleaned_schedule.append(semester)
            new_sem_count += 1
        else:
            cleanup_needed = True
    proposed_schedule = cleaned_schedule
    old_num_sems = num_sems
    num_sems = new_sem_count
    
    if cleanup_needed:
        return f"{old_num_sems} semesters not needed. New number of semesters automatically decreased to " + str(num_sems)
    else:
        return None


def scheduling_init():
    
    global prereq_chain
    global proposed_schedule
    global courses_taken
    global num_sems
    global credits_per_sem
    global credits_required
    
    courses_taken = set()
    prereq_chain = []
    proposed_schedule = []
    num_sems = 0
    credits_per_sem = 15
    credits_required = 0
