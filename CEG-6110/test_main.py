# from flask import Flask, render_template, request, redirect, url_for, flash
import accounts, scheduling, csv


scheduling.build_dicts()

# print(f"Length: {len(scheduling.course_catalog)}")
catalog = scheduling.course_catalog
# for k, v in catalog.items():      # testing that the catalog has been built correctly from the CSV file
#     print(f"{k} : {v}")
#     # print(m)
#     # print("")
#     # for c in m:
#     #     print(c)
#     #     print("\n")
# # print("Test line")
 

# if "MTH2310" and "PHY2410" in preqs["PHY2420"]:
#     print("found both")
# else:
#     print("NOT FOUND")


student1 = accounts.Student("Shane Martin", "martin12", "Password123$")

# student1.add_minor("Math Minor")
# math_minor = catalog["Math Minor"]
# print(math_minor)
# for item in math_minor:
#     print(f"Course: {item}")      # testing that course catalogs for each major/minor have been built to match the CSV files
 
# scheduling.build_chain(student1)
# scheduling.sort_prereqs_chain()
# chain = scheduling.prereq_chain

# for list in chain:
#     print(list)       # tests that the prereq chain was built correctly. displays each preq list in the chain
 
# student1.add_minor("Math Minor")
student1.add_major("CS Major")
# physics_minor = catalog["Physics Minor"]
# print(physics_minor)
courses = scheduling.courses
# for item in physics_minor:
    # print(f"Course: {item}..preqs:{courses[item].prereqs}")       # used to test that every course in degrees has a mapped prereq list
 
# scheduling.build_chain(student1)
# scheduling.sort_prereqs_chain()
# scheduling.build_empty_schedule(8)
# chain = scheduling.prereq_chain
# count = set()
# creds = 0
# for list in chain:
#     print(list)
#     for l in list:
#         count.add(l)

# for l in count:
#     creds += courses[l].credits
# print(f"total num courses: {len(count)}")
# print(f"total num cred: {creds}")

# print(f"\n total credits for maj/min combo: {scheduling.calc_total_credits()}")


# Testing the overall genartion of a schedule with generate_schedule(). then manually prints the schedule to terminal
sched = scheduling.generate_schedule(student1)
print(f"SUCCESS: {sched[0]}")
print(f"Message: {sched[1]}")
schedule = sched[2]
scount = 0
total_credits = 0
for sem in schedule:
    scount += 1
    cred = 0
    for s in sem:
        cred += courses[s].credits
        total_credits += courses[s].credits
    print(f"Semester {scount}: {sem} {cred} credits total.")
    print(f"Total credits in schedule: {total_credits}")
