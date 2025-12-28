import requests
import re
import sys
import json

year_catalog = []

try: 
    term_response = requests.get('https://api.umd.io/v1/courses/semesters')
    terms = term_response.json()
    year_catalog = [
            terms.pop(),
            terms.pop(),
            terms.pop(),
            terms.pop()
            ]
    print(year_catalog)
except requests.exceptions.Timeout as e:
        print(f"The request timed out: {e}")
        sys.exit(1)

except requests.exceptions.RequestException as e:
    print(f"An error occured with the request: {e}")
    sys.exit(1)
except Exception as e:
    print(f"An unexpected error occured: {e}")

courseGraph = {}
for term in year_catalog:
    page = 1

    while(1):
        try:
            print(f"On page {page}")
            response = requests.get(f'https://api.umd.io/v1/courses?page={page}&per_page=100')
            courses = response.json()
            if not courses:
                break
            for course in courses:
                course_id = course['course_id']
                relationships = course['relationships']
                prereq_string = relationships['prereqs']
                prereqs = []
                if prereq_string is not None:
                    course_pattern = r"[A-Z]{4}\d{3}(?:[A-Z]{1})?"
                    prereqs = re.findall(course_pattern, prereq_string)

                coreq_string = relationships['coreqs']
                coreqs = []
                if coreq_string is not None:
                    coreqs = re.findall(course_pattern, coreq_string)

                course_dict = {
                        "prereqs": prereqs,
                        "coreqs": coreqs,
                        "reverse_prereqs": []
                        }

                courseGraph[course_id] = course_dict
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

        
