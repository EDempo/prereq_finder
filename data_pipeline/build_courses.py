import requests
import re
import sys
import time
import json

try:
    response = requests.get('https://api.umd.io/v1/courses/list')
    courses = response.json()
    courseGraph = {}
    count = 0
    for course in courses:
        time.sleep(0.1)
        print(f"On course {count}")
        course = courses[0]
        course_id = course['course_id']
        try:
            courseResponse = requests.get(f'https://api.umd.io/v1/courses/{course_id}')
            courseDetails = courseResponse.json()
            course = courseDetails[0]
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
            count = count + 1

        except requests.exceptions.Timeout as e:
            print(f"The request timed out: {e}")
            sys.exit(1)
        except requests.exceptions.HTTPError as e:
            print(f"An HTTP error was thrown: {e}")
            sys.exit(1)
        except requests.exceptions.RequestException as e:
            print(f"An error occured with the request: {e}")
            continue
        except Exception as e:
            print(f"An unexpected error occured: {e}")
            continue

    for course_id in courseGraph:
        course = courseGraph[course_id]
        for prereq in course['prereqs']:
            if prereq  in courseGraph:
                reverse_course = courseGraph[prereq]
                if course_id not in reverse_course['reverse_prereqs']:
                    reverse_course['reverse_prereqs'].append(course_id)

    with open("../site/data/courses.json", "w") as f:
        json.dump(courseGraph, f, indent=2)

    
except requests.exceptions.Timeout as e:
    print(f"The request timed out: {e}")
    sys.exit(1)

except requests.exceptions.RequestException as e:
    print(f"An error occured with the request: {e}")
    sys.exit(1)
except Exception as e:
    print(f"An unexpected error occured: {e}")
