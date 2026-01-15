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
    print("PRINTING")
    if(isinstance(node, courseNode)):
        print(node.type)
        for i in node.children:
            if(isinstance(i, courseNode)):
                print_node(i)
            else:
                print(f"{i}\n")

def treeify(s):
    return(parse_expression(tokenize(s), 0))

def expand(match, op):
    print("ho\n")
    inner = match.group(1)
    courses = [c.strip() for c in inner.split(",")]
    print(f"this:{courses}")
    return "(" + op.join(courses) + ")"

def normalize(s):
    s = re.sub(r"1 course.*?from \(([^()]*)\)",
               lambda m: expand(m, " OR "),
               s,
               flags=re.IGNORECASE)

    s = re.sub(r"\(([^()]*?,[^()]*)\)",
               lambda m: expand(m, " AND "),
               s)


    return s

def tokenize(s: str) -> list:
    tokens = []
    s = normalize(s)
    s = re.sub(r"and\s+permission\s+of\s+.*?department\s*;?", "", s, flags = re.IGNORECASE)
    s = re.sub(r"\(", " LPAREN ", s) 
    s = re.sub(r"\)", " RPAREN ", s)
    punct = r"[;,\.-]"
    s = re.sub(punct, "", s)

    lst = s.split()
    course_pattern = r"[A-Z]{4}\d{3}(?:[A-Z]{1})?"
    for word in lst:
        if word in {"OR" , "AND" , "LPAREN" , "RPAREN" }:
            print(word)
            tokens.append(word)
        else:
            course = re.fullmatch(course_pattern, word)
            if course:
                tokens.append(course.group())

    print(f"TOKENS:\n{tokens}\n-------------------------------\n")
    return tokens

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

def parse_expression(tokens, i):
    node, i = parse_term(tokens, i)
    while i < len(tokens) and tokens[i] == "AND":
        i += 1
        right, i = parse_term(tokens, i)
        node = courseNode("AND", [node, right])
    print("parsed expression")
    print_node(node)
    return node, i

def parse_term(tokens, i):
    node, i = parse_factor(tokens, i)
    while tokens[i] == "OR":
        i += 1
        node = courseNode("OR", parse_factor(tokens, i))
    print("parsed term")
    print(node)
    return node, i

def parse_factor(tokens, i):
    course_pattern = r"[A-Z]{4}\d{3}(?:[A-Z]{1})?"
    if re.match(course_pattern, tokens[i]):
        lst = []
        lst.append(tokens[i])
        i += 1
        while re.match(course_pattern, tokens[i]):
            lst.append(tokens[i])
            i += 1
        return lst, i
    elif tokens[i] == "LPAREN":
        i += 1
        node = parse_expression(tokens, i)
        i += 1
        print("parsed factor")
        print(node)
        return node, i
    else:
        print("No factor\n")
        return None, i

## Factor Testing ##
def test_factor_course():
    tokens = ["CMSC351"]
    node, i = parse_factor(tokens, 0)

    assert node == "CMSC351", "test factor course failed"
    assert i == 1, "test factor course failed"

def test_factor_parens():
    tokens = ["LPAREN", "CMSC330", "RPAREN"]
    node, i = parse_factor(tokens, 0)

    assert node == "CMSC330", "test factor perens failed"
    assert i == 3, "test factor parens failed"

def test_term_or_chain():
    tokens = ["CMSC330", "OR", "CMSC351", "OR", "CMSC420"]
    node, i = parse_term(tokens, 0)

    expected = courseNode(
        "OR",
        [
            courseNode("OR", ["CMSC330", "CMSC351"]),
            "CMSC420"
        ]
    )

    assert node == expected, "or chain"
    assert i == len(tokens), "or chain"

def test_expression_and_or():
    tokens = [
        "CMSC330", "AND",
        "CMSC351", "OR",
        "CMSC420"
    ]

    node, i = parse_expression(tokens, 0)

    expected = courseNode(
        "AND",
        [
            "CMSC330",
            courseNode("OR", ["CMSC351", "CMSC420"])
        ]
    )

    assert node == expected, "and or"
    assert i == len(tokens), "and or"

def test_full_prereq():
    s = (
        "1 course with a minimum grade of C- from "
        "(CMSC414, CMSC417, CMSC420); "
        "and (ENEE350, CMSC330, and CMSC351)."
    )
    node, _ = treeify(s)

    expected = courseNode(
        "AND",
        [
            courseNode("OR", ["CMSC414", "CMSC417", "CMSC420"]),
            courseNode("AND", ["ENEE350", "CMSC330", "CMSC351"])
        ]
    )

    assert node == expected, "full"
    print_node(node)


