import requests
import json
import re
from collections import defaultdict

def fetch_sample_prereqs():
    """Fetch a sample of prerequisite strings from UMD.io API"""
    try:
        # Get current semester
        term_response = requests.get('https://api.umd.io/v1/courses/semesters')
        terms = term_response.json()
        current_term = terms[0] if terms else "202408"
        
        print(f"Using term: {current_term}")
        
        all_prereqs = []
        course_pattern = r"[A-Z]{4}\d{3}(?:[A-Z]{1})?"
        
        # Just get first few pages for analysis
        for page in range(1, 4):  # Pages 1-3
            try:
                print(f"Fetching page {page}...")
                response = requests.get(f'https://api.umd.io/v1/courses?semester={current_term}&page={page}&per_page=50')
                courses = response.json()
                
                if not courses:
                    break
                    
                for course in courses:
                    course_id = course['course_id']
                    relationships = course.get('relationships', {})
                    prereq_string = relationships.get('prereqs')
                    
                    if prereq_string and prereq_string.strip():
                        # Extract course IDs to verify pattern
                        courses_found = re.findall(course_pattern, prereq_string)
                        if courses_found:  # Only keep strings that have actual course IDs
                            all_prereqs.append({
                                'course_id': course_id,
                                'prereq_string': prereq_string.strip(),
                                'courses_found': courses_found
                            })
                
            except Exception as e:
                print(f"Error fetching page {page}: {e}")
                break
                
    except Exception as e:
        print(f"Error: {e}")
        return []
        
    return all_prereqs

def analyze_patterns(prereqs):
    """Analyze and categorize prerequisite patterns"""
    
    # Define pattern categories
    pattern_categories = {
        "Single Course": [
            "CMSC131",
            "MATH140", 
            "PHYS161"
        ],
        "Course with minimum grade": [
            "Minimum grade of C- in CMSC132",
            "A grade of C or better in MATH141",
            "CMSC330 with a minimum grade of C-"
        ],
        "1 from (courses)": [
            "1 course with a minimum grade of C- from (CMSC412, CMSC417, CMSC420)",
            "1 course from (ENEE322, ENEE323)",
            "1 course from (MATH240, MATH341)"
        ],
        "2 from (courses)": [
            "2 courses from (CMSC412, CMSC417, CMSC420, CMSC430)",
            "2 courses from (PHYS260, PHYS261)"
        ],
        "AND separated courses": [
            "CMSC132 and CMSC216",
            "MATH140 and MATH141", 
            "CMSC330 and CMSC351"
        ],
        "OR separated courses": [
            "CMSC132 or CMSC216",
            "ENEE322 or ENEE323",
            "MATH240 or MATH341"
        ],
        "Complex AND/OR combinations": [
            "CMSC132 and CMSC216 and (CMSC250 or CMSC256)",
            "(CMSC330 and CMSC351) or (ENEE350 and CMSC330)",
            "1 course from (CMSC412, CMSC417) and CMSC330"
        ],
        "Parentheses groups": [
            "(CMSC132 and CMSC216) and CMSC330",
            "CMSC131 and (MATH140 or MATH141)",
            "1 course from (CMSC412, CMSC417, CMSC420) and (CMSC330 or ENEE350)"
        ],
        "Permission + courses": [
            "CMSC132 and permission of department",
            "1 course from (CMSC412, CMSC417) and permission of CMNS-Computer Science department",
            "Junior standing and permission of instructor"
        ],
        "Test scores/AP credits": [
            "AP Calculus BC with a score of 4 or 5",
            "Math placement test score of 7",
            "SAT Math score of 600"
        ],
        "Credit/standing requirements": [
            "60 credits completed",
            "Junior standing or higher",
            "Graduate standing"
        ],
        "Department consent": [
            "Consent of instructor",
            "Department consent required"
        ]
    }
    
    # Analyze actual prereqs
    found_patterns = defaultdict(list)
    
    for prereq in prereqs:
        s = prereq['prereq_string'].lower()
        
        # Categorize based on content
        if "1 course" in s and "from (" in s:
            found_patterns["1 from (courses)"].append(prereq)
        elif "2 courses" in s and "from (" in s:
            found_patterns["2 from (courses)"].append(prereq)
        elif "3 courses" in s and "from (" in s:
            found_patterns["3 from (courses)"].append(prereq)
        elif " and " in s and " or " in s and "(" in s:
            found_patterns["Complex AND/OR combinations"].append(prereq)
        elif " and " in s and len(prereq['courses_found']) >= 2:
            found_patterns["AND separated courses"].append(prereq)
        elif " or " in s and len(prereq['courses_found']) >= 2:
            found_patterns["OR separated courses"].append(prereq)
        elif "permission" in s:
            found_patterns["Permission + courses"].append(prereq)
        elif "grade" in s:
            found_patterns["Course with minimum grade"].append(prereq)
        elif "test" in s or "score" in s or "ap " in s:
            found_patterns["Test scores/AP credits"].append(prereq)
        elif "credit" in s or "standing" in s:
            found_patterns["Credit/standing requirements"].append(prereq)
        elif "consent" in s:
            found_patterns["Department consent"].append(prereq)
        elif len(prereq['courses_found']) == 1:
            found_patterns["Single Course"].append(prereq)
        else:
            found_patterns["Other"].append(prereq)
    
    return found_patterns

def main():
    print("Fetching sample prerequisite strings...")
    prereqs = fetch_sample_prereqs()
    
    if not prereqs:
        print("No prerequisites found or error occurred")
        return
    
    print(f"Found {len(prereqs)} courses with prerequisites")
    
    # Analyze patterns
    patterns = analyze_patterns(prereqs)
    
    print("\n=== PREREQUISITE STRING TYPES ===\n")
    
    for pattern_type, courses in sorted(patterns.items()):
        print(f"## {pattern_type} ({len(courses)} courses)")
        
        # Show up to 3 examples
        for i, course in enumerate(courses[:3]):
            print(f"   **{course['course_id']}**: {course['prereq_string']}")
        
        if len(courses) > 3:
            print(f"   *... and {len(courses) - 3} more*")
        print()
    
    # Save analysis
    with open('sample_prereqs.json', 'w') as f:
        json.dump({
            'total': len(prereqs),
            'patterns': {k: len(v) for k, v in patterns.items()},
            'examples': {k: [{'course': v[i]['course_id'], 'string': v[i]['prereq_string']} 
                           for i in range(min(3, len(v)))] 
                        for k, v in patterns.items()}
        }, f, indent=2)
    
    print(f"Sample analysis saved to sample_prereqs.json")

if __name__ == "__main__":
    main()