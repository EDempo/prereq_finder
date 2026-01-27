# AGENTS.md

This file contains guidelines and commands for agentic coding agents working in this repository.

## Project Overview

This is a UMD (University of Maryland) prerequisite finder that consists of:
- **Data Pipeline** (`data_pipeline/`): Python scripts that parse course prerequisite strings and build course graphs
- **Frontend Site** (`site/`): Vanilla JavaScript web interface for exploring course prerequisites

## Build/Test Commands

### Python Data Pipeline
```bash
# Run tests (comprehensive prerequisite parsing tests)
cd data_pipeline && python3 test.py

# Build course graph from UMD API
cd data_pipeline && python3 build_courses.py

# Test individual prerequisite parsing
cd data_pipeline && python3 -c "import tree; print(tree.treeify('CMSC132 and CMSC216'))"
```

### JavaScript Frontend
```bash
# No build process required - static files
# Serve locally (optional):
cd site && python3 -m http.server 8000
# Then visit http://localhost:8000
```

### Environment Setup
```bash
# Python virtual environment (already exists)
cd data_pipeline && source .venv/bin/activate
pip install -r requirements.txt  # if needed

# Node.js (minimal - only for package.json)
npm install  # if dependencies are added
```

## Code Style Guidelines

### Python (Data Pipeline)

#### Imports
- Use standard imports at top of file
- Group imports: standard library, third-party, local modules
- Import local modules without `.py` extension: `import tree` (not `import tree.py`)

#### Naming Conventions
- **Classes**: `PascalCase` (e.g., `courseNode`)
- **Functions/Variables**: `snake_case` (e.g., `parse_expression`, `course_graph`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `COURSE_PATTERN`)
- **Private**: Use leading underscore for internal methods

#### Code Structure
- Follow the existing parser pattern: `tokenize() → parse_expression() → parse_term() → parse_factor()`
- Use type hints where beneficial: `def tokenize(s: str) -> list:`
- Keep functions focused and under 30 lines when possible
- Use descriptive variable names: `normalized_string`, `course_pattern`

#### Error Handling
- Use specific exceptions: `SyntaxError`, `requests.exceptions.RequestException`
- Include helpful error messages with context
- Handle network requests with try/except blocks for timeout and general errors

#### Documentation
- Use docstrings for complex functions
- Add inline comments for parsing logic and regex patterns
- Include example usage in test files

### JavaScript (Frontend)

#### Imports/Exports
- Use ES6 modules: `import { dfs } from "./graph.js"`
- Export functions explicitly: `export function dfs()`
- Use relative paths with `./` for local modules

#### Naming Conventions
- **Functions/Variables**: `camelCase` (e.g., `loadGraph`, `courseId`)
- **Constants**: `UPPER_SNAKE_CASE` for static values
- **DOM Elements**: Use descriptive names with element type: `courseInput`, `searchButton`

#### Code Structure
- Use async/await for API calls: `async function loadGraph()`
- Handle DOM events with addEventListener and proper error handling
- Separate data fetching from UI rendering logic
- Use modern DOM methods: `document.createElement`, `fetch`

#### Error Handling
- Validate user input before processing
- Display user-friendly error messages in DOM
- Use try/catch for network operations
- Check for null/undefined values from API responses

## Testing Guidelines

### Python Tests
- Tests are in `data_pipeline/test.py` using custom test framework
- Each test follows pattern: `test_prereqs(input_string, expected_tree, test_id)`
- Include edge cases: empty strings, malformed input, complex nested expressions
- Test both successful parsing and error conditions
- Run full test suite before committing changes

### Integration Testing
- Test the full pipeline: API → parsing → frontend display
- Verify course graph generation produces valid JSON
- Test frontend with sample data files
- Check cross-browser compatibility for frontend features

## File Organization

```
umd_prereq_finder/
├── data_pipeline/
│   ├── tree.py              # Core parsing logic
│   ├── build_courses.py     # API integration and graph building
│   ├── test.py             # Comprehensive test suite
│   ├── requirements.txt    # Python dependencies
│   └── .venv/              # Virtual environment
├── site/
│   ├── index.html          # Main HTML page
│   ├── style.css           # Styling
│   ├── src/
│   │   ├── ui.js           # Main UI logic
│   │   └── graph.js        # Graph traversal algorithms
│   └── data/
│       └── courses.json    # Generated course data
├── package.json            # Node.js metadata
└── README.md               # Project documentation
```

## Common Patterns

### Course ID Validation
```python
course_pattern = r"[A-Z]{4}\d{3}(?:[A-Z]{1})?"
if re.fullmatch(course_pattern, course_id):
    # Valid course ID
```

### Error Messages
- Be specific about what went wrong
- Include the problematic input when helpful
- Suggest corrective actions when possible

### API Integration
- Handle rate limiting and timeouts
- Cache responses when appropriate
- Validate API response structure before processing

## Development Workflow

1. **Before making changes**: Run existing tests to ensure baseline functionality
2. **When adding features**: Write tests first, then implement functionality
3. **When fixing bugs**: Add regression tests for the fix
4. **Before committing**: Run full test suite and verify frontend functionality
5. **After API changes**: Regenerate course data and test with new data structure

## Performance Considerations

- The frontend loads all course data at startup - keep JSON file size reasonable
- Use efficient graph traversal algorithms (DFS/BFS as appropriate)
- Cache parsed prerequisite trees to avoid re-parsing
- Consider pagination for large course lists in future iterations