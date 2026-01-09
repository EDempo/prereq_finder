import re

class courseNode:
    def __init__(self, type_, children):
        self.type = type_
        self.children = children

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

s = "1 course with a minimum grade of C- from (CMSC414, CMSC417, CMSC420, CMSC430, CMSC433, CMSC435, ENEE440, ENEE457); and permission of ENGR-Electrical & Computer Engineering department; and (ENEE350, CMSC330, and CMSC351).";
print(tokenize(s))
#for token in tokens:
#if LPAREN, while not right paren follow parse rules for all other token types
#if RPAREN, break out of the loop and just go back to the main parse loop
#if COURSE, add course to courseTree children
#if OR, call or parser; if no AND has been found yet, set type of node to OR
#if AND, call and parser; if AND is outside of PAREN, then  make type of courseTree AND

#I will have a paren flag letting me know if I'm in a set of parenthesis
#I will make a subtree for all tre
def parse(tokens: list) -> courseNode:
    for i in range(len(tokens)):
        if tokens[i] == "OR":
            parse_or(tokens[i:])
    return courseNode(None, [])


def parse_or(token_slice):

