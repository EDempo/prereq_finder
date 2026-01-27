# UMD Prerequisite String Types

This document catalogs all possible prerequisite string patterns found in the UMD.io courses API relationships data.

## Basic Patterns

### 1. Single Course
A single required course with no alternatives.
```
CMSC131
MATH140
PHYS161
```

### 2. Course with Minimum Grade
A single course with a specific grade requirement.
```
Minimum grade of C- in CMSC132
A grade of C or better in MATH141
CMSC330 with a minimum grade of C-
```

### 3. OR Separated Courses
Two or more courses where any one satisfies the requirement.
```
CMSC132 or CMSC216
ENEE322 or ENEE323
MATH240 or MATH341
AASP101 or AASP202
```

### 4. AND Separated Courses
Multiple courses where all must be completed.
```
CMSC132 and CMSC216
MATH140 and MATH141
CMSC330 and CMSC351
AASP386 and AASP297
```

## Selection Patterns

### 5. 1 from (Courses)
Select exactly one course from a list of alternatives.
```
1 course with a minimum grade of C- from (CMSC412, CMSC417, CMSC420, CMSC430, CMSC433, ENEE447)
1 course from (ENEE322, ENEE323)
1 course from (MATH240, MATH341)
```

### 6. 2 from (Courses)
Select exactly two courses from a list of alternatives.
```
2 courses from (CMSC412, CMSC417, CMSC420, CMSC430, CMSC433, ENEE447)
2 courses from (PHYS260, PHYS261)
```

### 7. 3 from (Courses)
Select exactly three courses from a list of alternatives.
```
3 courses from (CMSC412, CMSC417, CMSC420, CMSC430, CMSC433, ENEE447)
```

## Complex Combinations

### 8. Complex AND/OR with Parentheses
Combinations using parentheses to group AND/OR logic.
```
CMSC132 and (CMSC250 or CMSC256)
(CMSC330 and CMSC351) or (ENEE350 and CMSC330)
AASP101; and (ECON201 or ECON200)
BSCI105; or (BSCI170 and BSCI171)
```

### 9. Multiple Selection Groups
Multiple "1 from" groups combined with AND/OR logic.
```
1 course with a minimum grade of C- from (MATH240, MATH461, MATH341); and 1 course with a minimum grade of C- from (MATH340, MATH241); and 1 course with a minimum grade of C- from (CMSC106, CMSC131); and minimum grade of C- in MATH246
```

### 10. Mixed Selection + Specific Courses
Combination of selection patterns and specific course requirements.
```
ANSC101; and 1 course with a minimum grade of C- from (MATH120, MATH130, MATH136, MATH140)
CMSC466 or AMSC466; and MATH410
```

## Permission and Consent

### 11. Permission of Department
Department permission required, often combined with course requirements.
```
CMSC132 and permission of department
1 course from (CMSC412, CMSC417) and permission of CMNS-Computer Science department
Junior standing and permission of instructor
```

### 12. Permission of Instructor
Instructor permission required.
```
ANSC232; or permission of instructor
```

### 13. Department Consent
Consent from department or instructor.
```
Consent of instructor
Department consent required
```

## Standing and Credit Requirements

### 14. Class Standing
Specific academic standing requirements.
```
Junior standing or higher
Senior standing
Graduate standing
```

### 15. Credit Requirements
Specific number of credits completed.
```
60 credits completed
90 credits and junior standing
```

## Test Scores and External Credits

### 16. Test Score Requirements
Standardized test or placement test scores.
```
AP Calculus BC with a score of 4 or 5
Math placement test score of 7
SAT Math score of 600
```

### 17. AP/IB Credits
Advanced Placement or International Baccalaureate credits.
```
AP Calculus AB credit
IB Higher Level Mathematics
```

## Special Cases

### 18. Comparable Content
Courses with equivalent content may substitute.
```
MATH411; or students who have taken courses with comparable content may contact the department
```

### 19. Corequisite Mentioned
Courses that must be taken simultaneously.
```
CMSC131 (corequisite: MATH140)
```

### 20. Multiple Conditions
Complex strings with semicolon-separated conditions.
```
CMSC132; and permission of department; and junior standing
```

## Structural Patterns

### Punctuation Variations
- Periods: `CMSC131 or CMSC132.`
- Semicolons: `CMSC131; and MATH140`
- No punctuation: `CMSC131 or CMSC132`

### Case Variations
- Mixed case: `Minimum grade of C-`
- All caps: `CMSC131`
- Lowercase connectors: `and`, `or`

### Whitespace Patterns
- Standard: `CMSC131 and CMSC132`
- Extra spaces: `CMSC131  and  CMSC132`
- Line breaks (in longer strings)

## Parsing Complexity Levels

### Level 1: Simple
- Single course
- Simple OR/AND between 2-3 courses

### Level 2: Moderate
- Grade requirements
- "1 from" patterns
- Basic parentheses

### Level 3: Complex
- Multiple "1 from" groups
- Nested parentheses
- Mixed AND/OR logic

### Level 4: Very Complex
- Permission + course combinations
- Multiple condition types
- Comparable content clauses

## Frequency Analysis (Sample Data)

Based on analysis of UMD.io API data:

1. **OR separated courses**: ~35% of prereqs
2. **AND separated courses**: ~20% of prereqs  
3. **Single Course**: ~15% of prereqs
4. **Complex AND/OR combinations**: ~15% of prereqs
5. **1 from (courses)**: ~10% of prereqs
6. **Permission + courses**: ~5% of prereqs

## Notes for Parser Implementation

- The `normalize()` function should handle "1 course from" patterns
- Grade requirements can be stripped or preserved based on needs
- Permission clauses often appear at the end of strings
- Semicolons and periods should be treated as equivalent separators
- Course IDs follow pattern: `[A-Z]{4}\d{3}(?:[A-Z]{1})?`