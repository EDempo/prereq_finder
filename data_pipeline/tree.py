import re

class courseNode:
    def __init__(self, type_, children):
        self.type = type_
        self.children = children

    def __eq__(self, other):
        if not isinstance(other, courseNode):
            return False
        return self.type == other.type and self.children == other.children

    def __repr__(self):
        return f"{self.type}({self.children})"

def print_node(node):
    if(isinstance(node, courseNode)):
        print(f"{node.type},")
        print("[", end=" ")

        for i in range(len(node.children)):
                if i != 0:
                    print(",", end= " ")
                if(isinstance(node.children[i], courseNode)):
                    print_node(node.children[i])
                else:
                    print(f"{node.children[i]}", end="")
        print(" ]")

def treeify(s):
    node, _ = (parse_expression(tokenize(s), 0))
    return node

def expand(match, op):
    inner = match.group(1)
    courses = [c.strip() for c in inner.split(",")]
    for i in range(len(courses)):
        if "and" in courses[i]:
            courses[i] = courses[i].replace("and", "")

    return "(" + op.join(courses) + ")"

def normalize(s):
    s = re.sub(r"1 course.*?from \(([^()]*)\)",
               lambda m: expand(m, " OR "),
               s,
               flags=re.IGNORECASE)

    s = re.sub(r"\(([^()]*?,[^()]*)\)",
               lambda m: expand(m, " AND "),
               s)


    print(f"Normalized string is {s}")
    return s

def tokenize(s: str) -> list:
    tokens = []
    s = normalize(s)
    s = re.sub(r"and\s+permission\s+of\s+.*?department\s*;?", "", s, flags = re.IGNORECASE)
    s = re.sub(r"or\s+permission\s+of\s+.*?instructor\s*;?", "", s, flags = re.IGNORECASE)
    s = re.sub(r"\(", " LPAREN ", s) 
    s = re.sub(r"\)", " RPAREN ", s)
    punct = r"[;,\.-]"
    s = re.sub(punct, "", s)
    s = s.upper()
    print(f"this is s after all is s&d: {s}")

    lst = s.split()
    course_pattern = r"[A-Z]{4}\d{3}(?:[A-Z]{1})?"
    for word in lst:
        if word in {"OR" , "AND" , "LPAREN" , "RPAREN" }:
            tokens.append(word)
        else:
            course = re.fullmatch(course_pattern, word)
            if course:
                tokens.append(course.group())

    print(f"tokens is {tokens}")
    return tokens

#for token in tokens:
#if LPAREN, while not right paren follow parse rules for all other token types
#if RPAREN, break out of the loop and just go back to the main parse loop
#if COURSE, add course to courseTree children
#if OR, call or parser; if no AND has been found yet, set type of node to OR
#if AND, call and parser; if AND is outside of PAREN, then  make type of courseTree AND

#I will have a paren flag letting me know if I'm in a set of parenthesis
#I will make a subtree for all tree


#Expression takes highest precedence, then terms, then factors


#expression := term (AND term)*
def parse_expression(tokens, i):
    children = []
    node, i = parse_term(tokens, i)
    print(f"back, i is {i}")
    children.append(node)
    while i < len(tokens) and tokens[i] == "AND":
        print(f"in the expr while, i is {i}")
        print(f"remaining tokens are: {tokens[i:]}")
        i += 1
        right, i = parse_term(tokens, i)
        children.append(right)
        print(children)
        node = courseNode("AND", children)
        print("gonna print node now")
        print_node(node)

    print("returning my node now")
    print_node(node)
    return node, i


#term := factor (OR factor)*
def parse_term(tokens, i):
    children = []
    node, i = parse_factor(tokens, i)
    children.append(node)
    while i < len(tokens) and tokens[i] == "OR":
        i += 1
        right, i = parse_factor(tokens, i)
        children.append(right)
        node = courseNode("OR", children) 

    print("Post parse_term, node is:\n", end="")
    print_node(node)
    return node, i


#factor := COURSE/LPAREN expression RPAREN
def parse_factor(tokens, i):
    course_pattern = r"[A-Z]{4}\d{3}(?:[A-Z]{1})?"
    if tokens[i] == "LPAREN":
        i += 1
        node, i = parse_expression(tokens, i)
        print(f"i am in here {i}")
        if tokens[i] != "RPAREN":
            print(f"At index {i}, the token is {tokens[i]}")
            raise SyntaxError("Expected RPAREN")
        i += 1
        print(f"i is now {i}, print node is now: ", end="")
        print_node(node)
        return node, i
    elif re.fullmatch(course_pattern, tokens[i]):
        i += 1
        return tokens[i-1], i
    else:
        raise SyntaxError(f"Unexpected token: {tokens[i]}");


