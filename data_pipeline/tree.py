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

#def parse(tokens: list) -> dict:
   # courseTree = {}
   # for token in tokens:
   #     switch case
   # 


