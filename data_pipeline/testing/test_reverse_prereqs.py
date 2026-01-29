#!/usr/bin/env python3
"""
Test case to verify reverse prerequisites work correctly with new parsing rules.
This ensures that:
1. Forward prerequisites are parsed correctly 
2. Reverse prerequisite links are established properly
3. Course count tokens (like "2AMST") don't interfere with reverse lookups
4. Complex nested structures preserve correct relationships
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tree

def build_test_graph(courses_data):
    """
    Build a simplified course graph similar to build_courses.py logic
    """
    course_graph = {}
    
    # Initialize course entries
    for course_id in courses_data:
        course_graph[course_id] = {
            'prereqs': [],
            'coreqs': [],
            'reverse_prereqs': []
        }
    
    # Parse and add forward prerequisites
    for course_id, prereq_string in courses_data.items():
        try:
            node = tree.treeify(prereq_string)
            # Extract course IDs from parsed tree
            course_graph[course_id]['prereqs'] = extract_course_ids(node)
        except Exception as e:
            print(f"Error parsing {course_id}: {e}")
            course_graph[course_id]['prereqs'] = []
    
        print(f"Prereq List for {course_id} is {course_graph[course_id]['prereqs']}")
    # Build reverse prerequisites (same logic as build_cour#ses.py:111-117)
    for course_id in course_graph:
        print(f"dealing with {course_id}")
        course = course_graph[course_id]
        print(course)
        for prereq in course['prereqs']:
            print(prereq)
            if prereq in course_graph:
                print("hi")
                reverse_course = course_graph[prereq]
                if course_id not in reverse_course['reverse_prereqs']:
                    print("HIIIIIII")
                    reverse_course['reverse_prereqs'].append(course_id)
                    print(reverse_course['reverse_prereqs'])
            else:
                print(f"{prereq} does not exist in {course_graph}")
        print(f"Reverse-Prereq List for this course is {course_graph[course_id]['reverse_prereqs']}")
    
    return course_graph

def extract_course_ids(node):
    """
    Recursively extract valid course IDs from parsed tree
    Excludes tokens like "2AMST" that aren't valid course IDs
    """
    course_pattern = r"[A-Z]{4}\d{3}(?:[A-Z]{1})?"
    import re
    
    if isinstance(node, str):
        return [node] if re.fullmatch(course_pattern, node) else []
    
    if hasattr(node, 'children'):
        courses = []
        for child in node.children:
            courses.extend(extract_course_ids(child))
        return courses
    
    return []

def test_reverse_prereqs():
    """
    Test reverse prerequisite functionality with various course types
    """
    print("=== REVERSE PREREQUISITES TEST CASE ===")
    
    # Test data including course count requirements
    test_courses = {
        "CMSC216": "None.",
        "CMSC250": "None.",
        "MATH240": "None.",
        "MATH461": "None.",
        "MATH341": "None.",
        "MATH246": "None.",
        "AMST201": "None.",
        "CMSC330": "CMSC216 and CMSC250.",
        "CMSC351": "CMSC330 and CMSC350.",
        "MATH401": "1 course with a minimum grade of C- from (MATH240, MATH461, MATH341); and MATH246.",
        "AMST300": "Must have completed AMST201; and 2 courses in AMST.",
        "ENEE101": "None.",  # Course with no prereqs
        "TEST101": "CMSC351 or (MATH401 and permission of department)."
    }
    
    # Build graph
    course_graph = build_test_graph(test_courses)
    
    # Expected reverse relationships
    expected_reverse = {
        "CMSC216": ["CMSC330"],
        "CMSC250": ["CMSC330"], 
        "CMSC330": ["CMSC351", "TEST101"],
        "CMSC350": ["CMSC351"],
        "MATH240": ["MATH401"],
        "MATH461": ["MATH401"],
        "MATH341": ["MATH401"],
        "MATH246": ["MATH401"],
        "AMST201": ["AMST300"],
        # Note: "2AMST" should NOT appear in reverse prereqs
        "ENEE101": [],  # Should have no reverse prereqs
        "TEST101": []   # Has forward prereqs, no reverse expected in this test set
    }
    
    # Verify results
    print("\n--- VERIFICATION ---")
    all_passed = True
    
    for course_id, expected_rev in expected_reverse.items():
        actual_rev = sorted(course_graph.get(course_id, {}).get('reverse_prereqs', []))
        expected_rev_sorted = sorted(expected_rev)
        
        if actual_rev == expected_rev_sorted:
            print(f"✓ {course_id}: {actual_rev}")
        else:
            print(f"✗ {course_id}: Expected {expected_rev_sorted}, got {actual_rev}")
            all_passed = False
    
    # Specific tests for edge cases
    print("\n--- EDGE CASE VERIFICATION ---")
    
    # 1. Course count tokens should not create reverse links
    amst_entry = course_graph.get("AMST300", {})
    if "2AMST" not in [str(x) for x in amst_entry.get('prereqs', [])]:
        print("✓ Course count token '2AMST' handled correctly in forward prereqs")
    else:
        print("✗ Course count token '2AMST' incorrectly treated as course ID")
        all_passed = False
    
    # 2. ENEE101 should have no reverse prereqs
    enee_reverse = course_graph.get("ENEE101", {}).get('reverse_prereqs', [])
    if len(enee_reverse) == 0:
        print("✓ Course with no prereqs has empty reverse_prereqs")
    else:
        print(f"✗ Course with no prereqs incorrectly has reverse_prereqs: {enee_reverse}")
        all_passed = False
    
    # 3. Complex OR/AND nesting preserves relationships
    test101_reverse = course_graph.get("TEST101", {}).get('reverse_prereqs', [])
    if "TEST101" not in test101_reverse:
        print("✓ TEST101 correctly not in its own reverse_prereqs")
    else:
        print("✗ TEST101 incorrectly appears in its own reverse_prereqs")
        all_passed = False
    
    print(f"\n=== TEST RESULT: {'PASSED' if all_passed else 'FAILED'} ===")
    return all_passed

if __name__ == "__main__":
    test_reverse_prereqs()
