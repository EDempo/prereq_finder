import requests
import re
import sys
import json
import tree

year_catalog = []

#prereqs: 1 course with a minimum grade of C- from (CMSC412, CMSC417, CMSC420, CMSC430, CMSC433, ENEE447); and permission of CMNS-Computer Science department.
# {
# type: OR
#   children: [
#       courses: ["CMSC412", "CMSC417", "CMSC420", "CMSC430", "CMSC433", "ENEE447"]
#   ]
# }

#prereqs": "Minimum grade of C- in ENEE322 or ENEE323.
# {
# type: OR
#   children: [
#       courses: ["ENEE322", ENEE323"]
# }

# "prereqs": s = ("1 course with a minimum grade of C- from (CMSC414, CMSC417, CMSC420, CMSC430, CMSC433, CMSC435, ENEE440, ENEE457);" 
                # "and permission of ENGR-Electrical & Computer Engineering department;"
                # "and (ENEE350, CMSC330, and CMSC351)."
                #)
# {
# type: AND
#   children: [
#       {
#       type: OR
#           children: ["CMSC414", "CMSC417", "CMSC420", "CMSC430", "CMSC433", "CMSC435", "ENEE440", "ENEE457"]
#       },
#       {
#       type: AND
#           children: ["ENEE350", "CMSC330", "CMSC351"]
#       }
#   ]
# }


try: 
    term_response = requests.get('https://api.umd.io/v1/courses/semesters')
    terms = term_response.json()
    year_catalog = [
            terms.pop(),
            terms.pop(),
            terms.pop(),
            terms.pop()
            ]

except requests.exceptions.Timeout as e:
        print(f"The request timed out: {e}")
        sys.exit(1)

except requests.exceptions.RequestException as e:
    print(f"An error occured with the request: {e}")
    sys.exit(1)
except Exception as e:
    print(f"An unexpected error occured: {e}")

courseGraph = {}

# Reversing the year catalog means if there is a conflict for a course between two semesters, the more recent semester takes precedent


for term in reversed(year_catalog):
    print(f"TERM IS {term}")
    page = 1
    count = 1
    while(1):
        try:
            response = requests.get(f'https://api.umd.io/v1/courses?semester={term}&page={page}&per_page=100')
            courses = response.json()
            if not courses:
                break
            for course in courses:
                print(f"Course #{count}")
                course_id = course['course_id']
                relationships = course['relationships']
                prereq_string = relationships['prereqs']
                prereqs = []
                if prereq_string is not None:
                    node = tree.treeify(prereq_string)
                    prereqs = tree.flatten(node) if node is not None else [] 

                coreq_string = relationships['coreqs']
                coreqs = []
                if coreq_string is not None:
                    course_pattern = r"[A-Z]{4}\d{3}(?:[A-Z]{1})?"
                    coreqs = re.findall(course_pattern, coreq_string)

                course_dict = {
                        "prereqs": prereqs,
                        "coreqs": coreqs,
                        "reverse_prereqs": []
                        }

                if course_id not in courseGraph:
                    courseGraph[course_id] = course_dict
                print(f"DONE {count}")
                count += 1
            page += 1

        except requests.exceptions.Timeout as e:
            print(f"The request timed out: {e}")
            sys.exit(1)

        except requests.exceptions.RequestException as e:
            print(f"An error occured with the request: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"An unexpected error occured: {e}")

for course_id in courseGraph:
    course = courseGraph[course_id]
    for prereq in course['prereqs']:
        if prereq  in courseGraph:
            reverse_course = courseGraph[prereq]
            if course_id not in reverse_course['reverse_prereqs']:
                reverse_course['reverse_prereqs'].append(course_id)

with open("../site/data/courses.json", "w") as f:
    json.dump(courseGraph, f, indent=2)
