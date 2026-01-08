import re

def treeify(s):
    return parse(tokenize(s))

def tokenize(s: str) -> list:
    tokens = []
    s = re.sub("1 course.*?from", " OR ", s)
    s = re.sub(r"and\s+permission\s+of\s+.*?department\s*;?", "", s, flags = re.IGNORECASE)
    s = s.upper()
    s = re.sub(r"\(", " LPAREN ", s) 
    s = re.sub(r"\)", " RPAREN ", s)
    punct = r"[;,\.-]"
    s = re.sub(punct, "", s)
    print(f"This is the string: {s}\n")

    lst = s.split()
    course_pattern = r"[A-Z]{4}\d{3}(?:[A-Z]{1})?"
    for word in lst:
        if word in {"OR" , "AND" , "LPAREN" , "RPAREN" }:
            tokens.append(word)
        else:
            course = re.fullmatch(course_pattern, word)
            if course:
                tokens.append(course.group())
    return tokens

prereq1 = "prereqs: 1 course with a minimum grade of C- from (CMSC414, CMSC417, CMSC420, CMSC430, CMSC433, CMSC435, ENEE440, ENEE457); and permission of ENGR-Electrical & Computer Engineering department; and (ENEE350, CMSC330, and CMSC351)."
prereq2 = "prereqs: 1 course with a minimum grade of C- from (CMSC412, CMSC417, CMSC420, CMSC430, CMSC433, ENEE447); and permission of CMNS-Computer Science department."
prereq3 = "prereqs: Minimum grade of C- in ENEE322 or ENEE323."

print(f"{tokenize(prereq1)}\n")
print(f"{tokenize(prereq2)}\n")
print(f"{tokenize(prereq3)}\n")

def parse(tokens: list) -> dict:
    pass
   # courseTree = {}
   # for token in tokens:
   #     switch case
   # 


