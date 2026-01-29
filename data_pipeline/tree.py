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
    #print("Done frfr\n")
    return node

def expand(match, op):
    inner = match.group(1)
    courses = [c.strip() for c in inner.split(",")]
    for i in range(len(courses)):
        if "and" in courses[i]:
            courses[i] = courses[i].replace("and", "")

    return "(" + op.join(courses) + ")"

def normalize(s):

    # Remove common prefixes and boilerplate
    s = re.sub(r"Prerequisite:\s*", "", s, flags=re.IGNORECASE)
    s = re.sub(r"Must have completed\s*", "", s, flags=re.IGNORECASE)
    s = re.sub(r"Corequisite:\s*", "", s, flags=re.IGNORECASE)
    
    # Remove grade requirement prefixes but keep the course
    s = re.sub(r"Minimum grade of [A-D][+-]?\s+in\s+", "", s, flags=re.IGNORECASE)
    s = re.sub(r"minimum grade of [A-D][+-]?\s+in\s+", "", s, flags=re.IGNORECASE)
    s = re.sub(r"with a minimum grade of [A-D][+-]?\s+from\s+", "from ", s, flags=re.IGNORECASE)
    
    # Handle course count requirements - convert to parentheses format
    #s = re.sub(r"(\d+) courses? in\s+", r"(\1 courses in ", s, flags=re.IGNORECASE)
    s = re.sub(r"(and|or)? ([1-9]) courses? in\s+([A-Z]{4})\.", r"\1 \2\3", s, flags=re.IGNORECASE)
    s = re.sub(r"(and|or)?\s+must+have+appropriate\s+score", "", s, flags=re.IGNORECASE)
    
    # Remove student contact clauses (these don't affect parsing)
    s = re.sub(r"or\s+students\s+who\s+have\s+taken\s+courses\s+with\s+comparable\s+content\s+may\s+contact\s+the\s+department\s*[;,\.]?", "", s, flags=re.IGNORECASE)
    s = re.sub(r"students\s+who\s+have\s+taken\s+courses\s+with\s+comparable\s+content\s+may\s+contact\s+the\s+department\s*[;,\.]?", "", s, flags=re.IGNORECASE)
    
    # Standardize whitespace
    s = re.sub(r"\s+", " ", s)
    s = s.strip()

    s = re.sub(r"1 course.*?from \(([^()]*)\)",
               lambda m: expand(m, " OR "),
               s,
               flags=re.IGNORECASE)

    s = re.sub(r"\(([^()]*?,[^()]*)\)",
               lambda m: expand(m, " AND "),
               s)

    s = re.sub(r"and\s+permission\s+of\s+.*?department\s*;?", "PERMS", s, flags = re.IGNORECASE)
    s = re.sub(r"or\s+permission\s+of\s+.*?department\s*;?", "PERMS", s, flags = re.IGNORECASE)
    s = re.sub(r"or\s+permission\s+of\s+.*?instructor\s*;?", "PERMS", s, flags = re.IGNORECASE)
    s = re.sub(r"or\s+students\s+.*?department\s*;?", "", s, flags=re.IGNORECASE)
    s = re.sub(r"\(", " LPAREN ", s) 
    s = re.sub(r"\)", " RPAREN ", s)
    punct = r"[;,\.-]"
    s = re.sub(punct, "", s)
    s = s.upper()

    #print(f"Normalized string is {s}")
 
    return s

def tokenize(s: str) -> list:
    tokens = []
    #print(f"This is s {s}")
    s = normalize(s)
    #print(f"this is s after all is s&d: {s}")

    lst = s.split()
    course_pattern = r"[A-Z]{4}\d{3}(?:[A-Z]{1})?"
    courses_pattern = r"[1-9][A-Z]{4}"
    for word in lst:
        if word in {"OR" , "AND" , "LPAREN" , "RPAREN" }:
            tokens.append(word)
        else:
            course = re.fullmatch(course_pattern, word)
            if course:
                tokens.append(course.group())
            else:
                courses = re.fullmatch(courses_pattern, word)
                if courses:
                    tokens.append(courses.group())

    i = 0
    while(i <len(tokens)):
        if(tokens[i] == "LPAREN"):
            if i + 1 < len(tokens) and tokens[i + 1] == "RPAREN":
                print(i)
                print(i + 1)
                tokens.pop(i)
                tokens.pop(i)
                i += 2
            else:
                i += 1
        else:
            i += 1
    print(f"tokens is {tokens}")
    return tokens



#Expression takes highest precedence, then terms, then factors

#expression := term (AND term)*
def parse_expression(tokens, i):
    if(len(tokens) == 0):
        return None, i
    children = []
    node, i = parse_term(tokens, i)
    #print(f"back, i is {i}")
    children.append(node)
    while i < len(tokens) and tokens[i] == "AND":
        #print(f"in the expr while, i is {i}")
        #print(f"remaining tokens are: {tokens[i:]}")
        i += 1
        right, i = parse_term(tokens, i)
        children.append(right)
        #print(children)
        node = courseNode("AND", children)
        #print("gonna print node now")
        #print_node(node)

    #print("returning my node now")
    #print_node(node)
    return node, i


#term := factor (OR factor)*
def parse_term(tokens, i):
    if(len(tokens) == 0):
        return None, i
    children = []
    node, i = parse_factor(tokens, i)
    children.append(node)
    while i < len(tokens) and tokens[i] == "OR":
        i += 1
        right, i = parse_factor(tokens, i)
        children.append(right)
        node = courseNode("OR", children) 

    #print("Post parse_term, node is:\n", end="")
    #print_node(node)
    return node, i


#factor := COURSE/LPAREN expression RPAREN
def parse_factor(tokens, i):
    if(len(tokens) == 0):
        return None, i
    course_pattern = r"[A-Z]{4}\d{3}(?:[A-Z]{1})?"
    courses_pattern = r"[1-9][A-Z]{4}"
    if i < len(tokens):
        if tokens[i] == "LPAREN":
            i += 1
            node, i = parse_expression(tokens, i)
            #print(f"i am in here {i}")
            if i < len(tokens) and tokens[i] != "RPAREN":
                #print(f"At index {i}, the token is {tokens[i]}")
                raise SyntaxError("Expected RPAREN")
            i += 1
            #print(f"i is now {i}, print node is now: ", end="")
            #print_node(node)
            return node, i
        elif re.fullmatch(course_pattern, tokens[i]) or re.fullmatch(courses_pattern, tokens[i]):
            i += 1
            return tokens[i-1], i
        else:
            raise SyntaxError(f"Unexpected token: {tokens[i]}")
    else:
        raise IndexError(f"Index {i} is greater than token list length {len(tokens)}")


def flatten(node: courseNode) -> list:
    flattened = [node.type] if isinstance(node, courseNode) else node
    if(isinstance(flattened, str)):
        return flattened
    for c in node.children:
        if(isinstance(c, courseNode)):
            flattened.append(flatten(c))
        else:
            flattened.append(c)
    return flattened
