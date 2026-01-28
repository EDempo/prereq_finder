import re

def get_tokenization_rules():
    """
    Returns a list of regex replacement rules for tokenizing prerequisite strings.
    Each rule is a tuple of (pattern, replacement, flags).
    Rules are applied in order.
    """
    
    return [
        # Remove "Prerequisite:" prefix
        (r"Prerequisite:\s*", "", re.IGNORECASE),
        
        # Remove "Must have completed" and similar phrases
        (r"Must have completed\s*", "", re.IGNORECASE),
        
        # Handle minimum grade requirements
        (r"Minimum grade of [A-D][+-]?\s+in\s+", "", re.IGNORECASE),
        (r"minimum grade of [A-D][+-]?\s+in\s+", "", re.IGNORECASE),
        
        # Handle "1 course with a minimum grade of C- from" pattern
        (r"1 course with a minimum grade of C- from\s*", "ONEFROM(", re.IGNORECASE),
        (r"1 course in\s*", "ONEFROM(", re.IGNORECASE),
        (r"(\d+) courses in\s*", r"ONEFROM(\1,", re.IGNORECASE),
        
        # Handle permission requirements - replace with PERMS token
        (r"and\s+permission\s+of\s+[^;,\.]*department\s*[;,\.]?", " AND PERMS", re.IGNORECASE),
        (r"or\s+permission\s+of\s+[^;,\.]*department\s*[;,\.]?", " OR PERMS", re.IGNORECASE),
        (r"or\s+permission\s+of\s+instructor\s*[;,\.]?", " OR PERMS", re.IGNORECASE),
        (r";\s*and\s+permission\s+of\s+[^;,\.]*department\s*[;,\.]?", " AND PERMS", re.IGNORECASE),
        (r"permission\s+of\s+[^;,\.]*department\s*[;,\.]?", "PERMS", re.IGNORECASE),
        (r"permission\s+of\s+instructor\s*[;,\.]?", "PERMS", re.IGNORECASE),
        
        # Remove student contact clauses
        (r"or\s+students\s+who\s+have\s+taken\s+courses\s+with\s+comparable\s+content\s+may\s+contact\s+the\s+department\s*[;,\.]?", "", re.IGNORECASE),
        
        # Convert commas in course lists to OR within ONEFROM, otherwise to AND
        (r"ONEFROM\(([^)]*)\)", lambda m: "ONEFROM(" + m.group(1).replace(",", " OR ") + ")", re.IGNORECASE),
        
        # Handle commas between courses (outside of ONEFROM) - convert to AND
        (r"([A-Z]{4}\d{3}[A-Z]?)\s*,\s*([A-Z]{4}\d{3}[A-Z]?)", r"\1 AND \2", re.IGNORECASE),
        
        # Close ONEFROM parentheses
        (r"ONEFROM\(([^)]*)\)[;,\.]?", r"(\1)", re.IGNORECASE),
        
        # Add spaces around parentheses
        (r"\(", " ( ", re.IGNORECASE),
        (r"\)", " ) ", re.IGNORECASE),
        
        # Convert semicolons to AND
        (r"\s*;\s*", " AND ", re.IGNORECASE),
        
        # Convert "and" to AND (already spaced)
        (r"\s+and\s+", " AND ", re.IGNORECASE),
        
        # Convert "or" to OR (already spaced) 
        (r"\s+or\s+", " OR ", re.IGNORECASE),
        
        # Remove remaining punctuation
        (r"[,\.-]", "", re.IGNORECASE),
        
        # Clean up extra spaces
        (r"\s+", " ", re.IGNORECASE),
        (r"^\s+|\s+$", "", re.IGNORECASE),
         
        (r"\(", " LPAREN ", re.IGNORECASE),
        (r"\)", " RPAREN ", re.IGNORECASE),
    ]

def tokenize_prereq_string(s: str) -> list:
    """
    Apply tokenization rules and convert to token list.
    """
    # Apply all replacement rules
    for pattern, replacement, flags in get_tokenization_rules():
        if callable(replacement):
            s = re.sub(pattern, replacement, s, flags=flags)  # type: ignore
        else:
            s = re.sub(pattern, replacement, s, flags=flags)
    
    # Convert to uppercase and split
    s = s.upper()
    words = s.split()
    
    # Filter and validate tokens
    tokens = []
    course_pattern = r"[A-Z]{4}\d{3}[A-Z]?"
    
    for word in words:
        if word in {"OR", "AND", "(", ")"}:
            tokens.append(word)
        elif re.fullmatch(course_pattern, word):
            tokens.append(word)
        elif word == "PERMS":
            tokens.append(word)
    
    return tokens

def normalize_for_parsing(s: str) -> str:
    """
    Apply normalization rules but return string instead of tokens.
    Useful for debugging.
    """
    for pattern, replacement, flags in get_tokenization_rules():
        if callable(replacement):
            s = re.sub(pattern, replacement, s, flags=flags)  # type: ignore
        else:
            s = re.sub(pattern, replacement, s, flags=flags)
    
    return s.upper()
