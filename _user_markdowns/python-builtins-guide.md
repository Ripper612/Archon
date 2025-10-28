# Python Built-in Tools for Coding Agents

## Core Introspection & Analysis

### `ast` - Abstract Syntax Trees

```python
import ast

# Parse Python code safely
tree = ast.parse(source_code)
# Walk through all nodes
for node in ast.walk(tree):
    if isinstance(node, ast.FunctionDef):
        print(f"Found function: {node.name}")

```

### `inspect` - Runtime Object Inspection

```python
import inspect

# Get function signature
sig = inspect.signature(my_function)
# Get source code
source = inspect.getsource(my_function)
# Check if callable
inspect.iscoroutinefunction(func)

```

### `dis` - Bytecode Disassembly

```python
import dis

# Analyze function bytecode
dis.dis(my_function)

```

## File & Repository Operations

### `os` & `pathlib` - File System

```python
import os
from pathlib import Path

# Cross-platform path handling
path = Path("src") / "server" / "main.py"
if path.exists():
    content = path.read_text()

# Environment variables
env_var = os.getenv("DATABASE_URL")

```

### `glob` - Pattern Matching

```python
import glob

# Find all Python files
py_files = glob.glob("**/*.py", recursive=True)
# Find test files
test_files = glob.glob("tests/test_*.py")

```

### `shutil` - High-level File Operations

```python
import shutil

# Copy files/directories
shutil.copy2("source.py", "backup.py")
# Remove directory tree
shutil.rmtree("temp_dir")

```

## Data Structures & Processing

### `collections` - Advanced Containers

```python
from collections import defaultdict, Counter, deque

# Group items efficiently
by_type = defaultdict(list)
for item in items:
    by_type[item.type].append(item)

# Count occurrences
word_counts = Counter(words)

# FIFO queue
queue = deque()

```

### `itertools` - Iterator Tools

```python
import itertools

# Generate combinations
for combo in itertools.combinations(items, 2):
    process_pair(combo)

# Group consecutive items
for key, group in itertools.groupby(sorted(items), key_func):
    process_group(key, list(group))

```

### `functools` - Function Tools

```python
from functools import lru_cache, partial

# Cache expensive operations
@lru_cache(maxsize=128)
def expensive_calculation(x):
    return x ** 2

# Partial function application
add_five = partial(operator.add, 5)

```

## Testing & Debugging

### `unittest` - Built-in Testing

```python
import unittest

class TestMyCode(unittest.TestCase):
    def test_functionality(self):
        self.assertEqual(my_function(2), 4)

if __name__ == "__main__":
    unittest.main()

```

### `pdb` - Python Debugger

```python
import pdb

# Set breakpoint
pdb.set_trace()

# Post-mortem debugging
try:
    risky_operation()
except Exception:
    pdb.post_mortem()

```

### `logging` - Structured Logging

```python
import logging

# Configure logging
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s')

# Log messages
logging.info("Processing started")
logging.error("An error occurred", exc_info=True)

```

## System & Utilities

### `sys` - System Interface

```python
import sys

# Command line arguments
script_name = sys.argv[0]
args = sys.argv[1:]

# Exit with code
sys.exit(0)

# Python path
sys.path.append("/custom/path")

```

### `json` - JSON Processing

```python
import json

# Parse JSON
data = json.loads(json_string)
# Serialize to JSON
json_str = json.dumps(data, indent=2)

```

### `re` - Regular Expressions

```python
import re

# Search patterns
if re.search(r"def \w+\(", line):
    print("Found function definition")

# Extract groups
match = re.match(r"(\w+): (\d+)", line)
if match:
    name, value = match.groups()

```

### `pickle` - Object Serialization

```python
import pickle

# Serialize object
with open("data.pkl", "wb") as f:
    pickle.dump(my_object, f)

# Deserialize
with open("data.pkl", "rb") as f:
    loaded = pickle.load(f)

```

## Best Practices for Coding Agents

1. **Use `ast` for safe code analysis** instead of regex when possible
2. **Combine `pathlib` + `glob`** for repository file operations
3. **Leverage `collections`** for efficient data grouping and counting
4. **Apply `functools.lru_cache`** to expensive computations
5. **Use `logging`** for structured output and debugging
6. **Write `unittest` cases** to validate changes before applying
7. **Use `json`** for configuration and data exchange
8. **Prefer `pathlib`** over `os.path` for better code readability

## Common Agent Workflows

### Code Analysis

```python
import ast
from pathlib import Path

def analyze_codebase(root_path: str):
    stats = defaultdict(int)
    for py_file in Path(root_path).glob("**/*.py"):
        try:
            tree = ast.parse(py_file.read_text())
            stats["files"] += 1
            stats["classes"] += len([n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)])
            stats["functions"] += len([n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)])
        except SyntaxError:
            stats["errors"] += 1
    return dict(stats)

```

### File Processing

```python
from pathlib import Path
import shutil
import logging

def backup_and_process(files: list[str], backup_dir: str):
    backup_path = Path(backup_dir)
    backup_path.mkdir(exist_ok=True)

    for file_path in files:
        path = Path(file_path)
        if path.exists():
            # Create backup
            backup_file = backup_path / f"{path.name}.backup"
            shutil.copy2(path, backup_file)
            logging.info(f"Backed up {file_path} to {backup_file}")

            # Process file
            process_file(path)

```

### Testing Validation

```python
import unittest
import tempfile
from pathlib import Path

class CodeChangeTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def test_change_validation(self):
        # Test code changes before applying
        test_file = Path(self.temp_dir) / "test.py"
        test_file.write_text("def add(a, b): return a + b")

        # Run validation
        result = validate_change(test_file)
        self.assertTrue(result["syntax_valid"])
        self.assertTrue(result["tests_pass"])

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

```
