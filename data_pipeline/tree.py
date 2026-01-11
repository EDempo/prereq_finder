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

s = "1 course with a minimum grade of C- from (CMSC414, CMSC417, CMSC420, CMSC430, CMSC433, CMSC435, ENEE440, ENEE457); and permission of ENGR-Electrical & Computer Engineering department; and (ENEE350, CMSC330, and CMSC351)."
print(tokenize(s))
#for token in tokens:
#if LPAREN, while not right paren follow parse rules for all other token types
#if RPAREN, break out of the loop and just go back to the main parse loop
#if COURSE, add course to courseTree children
#if OR, call or parser; if no AND has been found yet, set type of node to OR
#if AND, call and parser; if AND is outside of PAREN, then  make type of courseTree AND

#I will have a paren flag letting me know if I'm in a set of parenthesis
#I will make a subtree for all tree

#expression := term (AND term)*
#term       := factor (OR factor)*
#factor     := COURSE/LPAREN expression RPAREN

#Expression takes highest precedence, then terms, then factors


def parse(tokens: list) -> courseNode:
    children = []
    type = None
    i = 0
    while i < len(tokens): 
        if tokens[i] == "OR":
            if(type != "AND"):
                type = "OR"
            or_node, i = parse_or(tokens, i + 1)
            children.append(or_node)
        elif tokens[i] == "AND":
            type = "AND"
            and_node, i = parse_and(tokens, i + 1)
            children.append(and_node)
 
        else:
            children.append(tokens[i])
        i += 1
    return courseNode(type, children)


def parse_or(tokens, i):
    children = []
    if tokens[i] == "LPAREN":
        i += 1
    while tokens[i] != "RPAREN" and i < len(tokens):
        if tokens[i] == "OR" and tokens[i+1] == "LPAREN":
            children.append(parse_or(tokens, i + 1))
        elif tokens[i] == "AND" and tokens[i+1] == "RPAREN":
            children.append(parse_and(tokens, i + 1))
        else:
            children.append(tokens[i])
        i += 1
    return (courseNode("OR", children)), i


    
        
        

        

def parse_and(tokens, i):
    children = []
    if tokens[i] == "LPAREN":
        i += 1
    while tokens[i] != "RPAREN" and i < len(tokens):
        if tokens[i] == "OR":
            if(tokens[i+1] == "LPAREN"):
                children.append(parse_or(tokens, i + 1))
        elif tokens[i] == "AND":
            if(tokens[i+1] == "LPAREN"):
                children.append(parse_and(tokens, i+1 ))
        else:
            children.append(tokens[i])
        i += 1
    return (courseNode("AND", children)), i
