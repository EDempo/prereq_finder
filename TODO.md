UMD Course Prereq Finder – Full App Roadmap
Setup & Project Foundation  - DONE
Graph Logic - DONE
Basic UI Integration - DONE
Full Traversal & Coreqs - DONE
Extend the app to show all course relationships - DONE
UI Polish & Usability - in progress with changes to main stuff
Implement topological sorting rather than normal DFS to make UX better - DONe
-- Finish rendering mechanics (updating CSS for the subsequent courses, adding the sortest lists, etc)
Make the app dynamic, always up-to-date, and ready for public access. -not yet
Implement caching of the course graph to avoid multiple fetches.

Task 1: Logic Handling
[✔] Decide on a minimal prereq logic structure (COURSE / AND / OR)
[ ] Update Python prereq parser to output a logic tree instead of raw strings
[ ] Add a helper to flatten logic trees into a simple course list for graph traversal
[ ] Store both:
    - prereq_logic (tree)
    - prereq_flat (list of courses)
[ ] Use prereq_flat for DFS / topo sorting (no UI changes yet)
[ ] Add a JS renderer that converts prereq_logic into human-readable text:
    - "(A or B)"
    - "(one of A, B, C)"
[ ] Display logic text in the prereqs panel without changing layout

Task 2: Depth Labling
[ ] Modify graph traversal to track parent course during DFS
[ ] Store prereq entries as objects instead of strings:
    - { course, parent, depth }
[ ] Keep coreqs depth-free (always depth 1)
[ ] Use negative depth values for reverse prereqs if needed
[ ] Update ui.js render() to:
    - show course name normally
    - show "(prereq of X)" as a separate <span>
[ ] Style the span with CSS (smaller, italic, muted)
[ ] Do NOT encode depth or parent info into strings

Task 3: Fix Bugs
[ ] One bug I know of: CMSC412 has ENEE447 as a prereq even though the original prereq graph 
doesng contain 447, get to the bottom of that (might get fixed when task 1 is finished)
