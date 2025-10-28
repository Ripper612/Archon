# Advanced Python Tools for Coding Agents

## Overview

This guide covers essential Python libraries that complement the built-in standard library, discovered through research in the awesome-python repository and other sources. These tools significantly enhance coding agents' capabilities for analysis, refactoring, and testing.

## 🔍 Code Analysis & Quality

### `boltons` - Pure-Python Standard Library Extensions

**Best for**: Filling gaps in the standard library with high-quality utilities.

```python
from boltons.iterutils import chunked, pairwise, unique_everseen
from boltons.cacheutils import cachedproperty, LRIACache

# Process files in batches for memory efficiency
def analyze_codebase_batch(files, batch_size=10):
    for batch in chunked(files, batch_size):
        results = [analyze_file(f) for f in batch]
        yield results

# Smart caching for expensive operations
class CodeAnalyzer:
    @cachedproperty
    def file_patterns(self):
        """Computed once, cached forever"""
        return compile_regex_patterns()

    def analyze(self, code):Interactive prompts → click.prompt + click.confirm
        patterns = self.file_patterns
        return find_issues(code, patterns)
```

**Agent Use Case**: Process large codebases without memory issues using `chunked()`, cache analysis patterns with `cachedproperty()`.

### `more-itertools` - Extended Iterator Tools

**Best for**: Advanced iteration patterns beyond basic `itertools`.

```python
from more_itertools import windowed, unique_everseen, flatten, grouper

# Sliding window analysis for code patterns
def detect_code_smells(lines):
    """Look for patterns spanning multiple lines"""
    for window in windowed(lines, 5):
        if is_long_parameter_list(window):
            yield "Long parameter list detected"

# Remove duplicates while preserving order
def unique_dependencies(imports):
    """Clean up import lists"""
    return list(unique_everseen(flatten(imports)))

# Group analysis results
def group_by_severity(issues):
    """Organize issues by severity level"""
    return grouper(issues, key=lambda x: x.severity)
```

**Agent Use Case**: Pattern detection across multiple lines, deduplication of analysis results.

## 🛠️ Built-in Class Enhancements

### `funcy` - Functional Programming Utilities

**Best for**: Functional programming patterns and data pipelines.

```python
from funcy import partial, compose, lmap, lfilter, group_by

# Create reusable analysis functions
analyze_python_files = partial(find_files, extension='.py')
analyze_js_files = partial(find_files, extension='.js')

# Data processing pipeline
process_codebase = compose(
    lmap(extract_functions),      # Extract functions from each file
    flatten,                      # Flatten nested lists
    lfilter(lambda f: len(f) > 5), # Filter short functions
    group_by(lambda f: f.complexity) # Group by complexity
)

# Quick data transformations
complex_functions = lfilter(lambda f: f.complexity > 10, all_functions)
function_names = lmap(lambda f: f.name, complex_functions)
```

**Agent Use Case**: Build composable analysis pipelines, create specialized analysis functions with `partial()`.

## 📁 Advanced File & Path Operations

### Enhanced Path Handling

**Best for**: Sophisticated file system operations.

```python
from pathlib import Path
import os

def find_project_files(root_path: str, patterns: list[str]) -> list[Path]:
    """Find files matching multiple patterns"""
    root = Path(root_path)
    files = []

    for pattern in patterns:
        files.extend(root.glob(f"**/{pattern}"))

    return sorted(set(files))  # Remove duplicates

def analyze_file_structure(project_root: str):
    """Analyze project organization"""
    root = Path(project_root)

    structure = {
        'python_files': len(list(root.glob('**/*.py'))),
        'test_files': len(list(root.glob('**/test_*.py'))),
        'config_files': len(list(root.glob('**/config*.py'))),
        'readme_files': list(root.glob('**/README*')),
    }

    return structure
```

**Agent Use Case**: Complex file discovery patterns, project structure analysis.

## 🖥️ Command-Line Interfaces

### `click` - Beautiful CLI Applications

**Best for**: Professional command-line tools for coding agents.

```python
import click
from pathlib import Path

@click.group()
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
@click.option('--config', type=click.Path(exists=True), help='Config file path')
@click.pass_context
def analyze(ctx, verbose, config):
    """Code analysis toolkit"""
    ctx.ensure_object(dict)
    ctx.obj['VERBOSE'] = verbose
    ctx.obj['CONFIG'] = config

@analyze.command()
@click.argument('source', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), help='Output file')
@click.option('--format', type=click.Choice(['json', 'html', 'text']), default='json')
@click.pass_context
def codebase(ctx, source, output, format):
    """Analyze entire codebase"""
    if ctx.obj['VERBOSE']:
        click.echo(f"Analyzing {source}")

    results = analyze_codebase(source)

    if format == 'json':
        import json
        output_data = json.dumps(results, indent=2)
    elif format == 'html':
        output_data = generate_html_report(results)
    else:
        output_data = format_text_report(results)

    if output:
        Path(output).write_text(output_data)
    else:
        click.echo(output_data)
```

**Agent Use Case**: Create professional CLI tools for code analysis with proper help, validation, and output formatting.

### `rich` - Rich Terminal Output

**Best for**: Beautiful console output for analysis results.

```python
from rich.console import Console
from rich.table import Table
from rich.progress import track, Progress
from rich.panel import Panel
from rich.columns import Columns

console = Console()

def display_analysis_summary(results):
    """Display analysis results in a beautiful table"""
    table = Table("Category", "Files", "Issues", "Score")
    table.add_row("Security", "12", "3", "[red]High Risk[/red]")
    table.add_row("Performance", "8", "1", "[yellow]Medium Risk[/yellow]")
    table.add_row("Maintainability", "15", "7", "[green]Good[/green]")

    console.print(Panel(table, title="Code Analysis Report"))

def analyze_with_progress(files):
    """Show progress during analysis"""
    with Progress() as progress:
        task = progress.add_task("Analyzing files...", total=len(files))

        results = []
        for file in files:
            result = analyze_file(file)
            results.append(result)
            progress.advance(task)

        return results

def display_file_grid(files):
    """Display files in a grid layout"""
    panels = [Panel(f"[bold]{f.name}[/bold]\n{f.stat().st_size} bytes")
              for f in files[:9]]  # Show first 9 files

    console.print(Columns(panels, equal=True))
```

**Agent Use Case**: Create visually appealing analysis reports, show progress for long-running tasks, organize information in tables and grids.

## 🧪 Testing & Validation

### `hypothesis` - Property-Based Testing

**Best for**: Comprehensive testing of code analysis functions.

```python
from hypothesis import given, strategies as st, settings
import ast

@given(st.text(min_size=10, max_size=1000))
def test_code_parser_handles_any_input(code):
    """Test that parser handles any input gracefully"""
    try:
        tree = ast.parse(code)
        # If parsing succeeds, verify it's valid
        assert isinstance(tree, ast.Module)
    except SyntaxError:
        # Syntax errors are acceptable
        pass

@given(st.lists(st.integers(min_value=0, max_value=100)))
def test_sorting_algorithm_stability(data):
    """Test that sorting preserves order for equal elements"""
    result = stable_sort(data)
    assert len(result) == len(data)
    assert all(result[i] <= result[i+1] for i in range(len(result)-1))

@settings(max_examples=1000)
@given(st.dictionaries(st.text(), st.integers()))
def test_analysis_result_consistency(config):
    """Test analysis works with various configurations"""
    analyzer = CodeAnalyzer(config)
    result = analyzer.analyze("def test(): pass")

    assert 'complexity' in result
    assert 'issues' in result
    assert isinstance(result['issues'], list)
```

**Agent Use Case**: Test code analysis functions against edge cases, ensure robustness with various inputs.

## 🔧 Configuration & Settings

### `pydantic` - Type-Safe Configuration

**Best for**: Robust configuration management for coding agents.

```python
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from pathlib import Path

class AnalysisConfig(BaseModel):
    """Configuration for code analysis"""

    # File discovery
    include_patterns: List[str] = Field(default_factory=lambda: ['*.py'])
    exclude_patterns: List[str] = Field(default_factory=lambda: ['test_*', '__pycache__'])

    # Analysis settings
    max_file_size: int = Field(default=1_000_000, gt=0)
    max_complexity: int = Field(default=10, ge=1, le=50)
    min_function_length: int = Field(default=5, ge=1)

    # Output settings
    output_format: str = Field(default='json', regex='^(json|html|text)$')
    output_file: Optional[Path] = None
    verbose: bool = False

    # Advanced options
    enable_ast_analysis: bool = True
    enable_import_analysis: bool = True
    custom_rules: Dict[str, Any] = Field(default_factory=dict)

    @validator('output_file')
    def validate_output_file(cls, v):
        if v and not v.parent.exists():
            raise ValueError(f"Output directory {v.parent} does not exist")
        return v

    @validator('exclude_patterns')
    def validate_patterns(cls, v):
        for pattern in v:
            if not pattern or ' ' in pattern:
                raise ValueError(f"Invalid exclude pattern: {pattern}")
        return v

# Usage
config = AnalysisConfig(
    max_complexity=15,
    output_format='html',
    exclude_patterns=['test_*', 'migrations']
)

# Load from environment variables
import os
config_from_env = AnalysisConfig(
    max_file_size=int(os.getenv('ANALYSIS_MAX_FILE_SIZE', '1000000')),
    verbose=os.getenv('ANALYSIS_VERBOSE', 'false').lower() == 'true'
)
```

**Agent Use Case**: Type-safe configuration with validation, environment variable support, complex nested settings.

## 📊 Data Visualization & Reporting

### `pandas` - Data Analysis for Code Metrics

**Best for**: Analyzing large codebases and generating insights.

```python
import pandas as pd
from pathlib import Path

def analyze_codebase_metrics(root_path: str) -> pd.DataFrame:
    """Analyze codebase and return metrics as DataFrame"""

    data = []
    for py_file in Path(root_path).glob('**/*.py'):
        metrics = analyze_file_metrics(py_file)

        data.append({
            'file': str(py_file),
            'lines': metrics['lines'],
            'functions': len(metrics['functions']),
            'classes': len(metrics['classes']),
            'complexity': metrics['complexity'],
            'imports': len(metrics['imports'])
        })

    df = pd.DataFrame(data)
    return df

def generate_insights(df: pd.DataFrame):
    """Generate insights from codebase analysis"""

    insights = {}

    # Complexity analysis
    insights['high_complexity'] = df[df['complexity'] > 15]
    insights['avg_complexity'] = df['complexity'].mean()
    insights['complexity_std'] = df['complexity'].std()

    # Size analysis
    insights['largest_files'] = df.nlargest(10, 'lines')
    insights['total_lines'] = df['lines'].sum()

    # Function density
    df['functions_per_line'] = df['functions'] / df['lines']
    insights['function_density'] = df['functions_per_line'].describe()

    return insights

# Usage
df = analyze_codebase_metrics('./src')
insights = generate_insights(df)

print(f"Total files: {len(df)}")
print(f"Average complexity: {insights['avg_complexity']:.2f}")
print(f"Files with high complexity: {len(insights['high_complexity'])}")
```

**Agent Use Case**: Statistical analysis of code metrics, trend identification, comparative analysis across projects.

## 🚀 Performance & Optimization

### `numba` - JIT Compilation

**Best for**: Speeding up performance-critical analysis functions.

```python
from numba import jit, types
import numpy as np

@jit(nopython=True)
def fast_pattern_matching(code_lines, patterns):
    """JIT-compiled pattern matching for speed"""
    matches = []

    for i, line in enumerate(code_lines):
        line_bytes = line.encode('utf-8')

        for pattern in patterns:
            pattern_bytes = pattern.encode('utf-8')
            if pattern_bytes in line_bytes:
                matches.append((i, pattern))

    return matches

@jit
def calculate_code_complexity(ast_tree):
    """Fast complexity calculation"""
    complexity = 0

    # Count control structures
    for node in ast.walk(ast_tree):
        if isinstance(node, (ast.If, ast.For, ast.While)):
            complexity += 1
        elif isinstance(node, ast.Try):
            complexity += 2

    return complexity

# Usage
patterns = ['TODO', 'FIXME', 'XXX']
lines = ['# TODO: fix this', 'def func():', '# FIXME']

matches = fast_pattern_matching(lines, patterns)
print(f"Found {len(matches)} pattern matches")
```

**Agent Use Case**: Speed up analysis of large codebases, optimize frequently called functions.

## 🐛 Debugging & Profiling

### `icecream` - Better Debugging

**Best for**: Enhanced debugging output compared to print().

```python
from icecream import ic

def analyze_function_complexity(func):
    """Analyze function complexity with detailed debugging"""

    ic(func.__name__)  # Shows: func.__name__: 'analyze_function_complexity'
    ic(func.__code__.co_varnames)  # Shows: func.__code__.co_varnames: ('func', 'source')

    source = inspect.getsource(func)
    ic(len(source))  # Shows: len(source): 245

    tree = ast.parse(source)
    ic(len(list(ast.walk(tree))))  # Shows: len(list(ast.walk(tree))): 42

    complexity = calculate_complexity(tree)
    ic(complexity)  # Shows: complexity: 8

    return complexity

# Debug analysis pipeline
def debug_analysis_pipeline(codebase_path):
    """Debug the entire analysis pipeline"""

    ic("Starting codebase analysis")
    files = find_python_files(codebase_path)
    ic(f"Found {len(files)} Python files")

    results = []
    for i, file in enumerate(files):
        ic(f"Analyzing file {i+1}/{len(files)}: {file.name}")
        result = analyze_file(file)
        results.append(result)

        if i % 10 == 0:  # Progress update every 10 files
            ic(f"Processed {i+1} files, {len(results)} results")

    ic("Analysis complete")
    return results
```

**Agent Use Case**: Detailed debugging output, trace analysis pipeline execution, inspect intermediate values.

### `memory_profiler` - Memory Usage Analysis

**Best for**: Monitoring memory usage during analysis.

```python
from memory_profiler import profile, memory_usage
import gc

@profile
def analyze_large_codebase(codebase_path):
    """Monitor memory usage during large codebase analysis"""

    print("Loading all Python files...")
    files = list(find_python_files(codebase_path))
    print(f"Found {len(files)} files")

    print("Parsing AST trees...")
    ast_trees = []
    for file in files:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read())
                ast_trees.append(tree)
        except (SyntaxError, UnicodeDecodeError):
            continue

    print(f"Parsed {len(ast_trees)} AST trees")

    print("Analyzing code patterns...")
    results = analyze_patterns(ast_trees)

    print("Generating report...")
    report = generate_report(results)

    return report

def monitor_memory_usage(func, *args, **kwargs):
    """Monitor memory usage of a function"""

    print("Starting memory monitoring...")

    # Get initial memory
    initial_memory = memory_usage()[0]
    print(f"Initial memory: {initial_memory:.2f} MB")

    # Run function and monitor memory
    mem_usage = memory_usage((func, args, kwargs), interval=0.1)

    final_memory = memory_usage()[0]
    peak_memory = max(mem_usage)

    print(f"Final memory: {final_memory:.2f} MB")
    print(f"Peak memory: {peak_memory:.2f} MB")
    print(f"Memory increase: {final_memory - initial_memory:.2f} MB")

    return mem_usage[-1]  # Return the function result

# Usage
result = monitor_memory_usage(analyze_large_codebase, './large_project')
```

**Agent Use Case**: Monitor memory usage of analysis functions, detect memory leaks, optimize for large codebases.

## 📈 Recommended Agent Stack

### Core Analysis Toolkit

```python
# Essential imports for a coding agent
import ast
import inspect
from pathlib import Path
from typing import List, Dict, Any

# Enhanced standard library
from boltons.iterutils import chunked
from boltons.cacheutils import cachedproperty
from more_itertools import windowed, unique_everseen
from funcy import compose, partial, lmap, lfilter

# CLI and output
import click
from rich.console import Console
from rich.table import Table

# Configuration and validation
from pydantic import BaseModel, Field

# Performance
from functools import lru_cache
from numba import jit

class AdvancedCodeAnalyzer:
    """Advanced coding agent with full toolkit"""

    def __init__(self, console=None):
        self.console = console or Console()

    @cachedproperty
    def analysis_patterns(self):
        """Pre-compiled analysis patterns"""
        return self._compile_patterns()

    @lru_cache(maxsize=100)
    def analyze_file(self, file_path: str) -> Dict[str, Any]:
        """Analyze a single file with caching"""
        path = Path(file_path)

        try:
            tree = ast.parse(path.read_text())
            return self._analyze_ast(tree, str(path))
        except SyntaxError as e:
            return {'error': f'Syntax error: {e}'}

    def analyze_codebase(self, root_path: str, batch_size: int = 20) -> Dict[str, Any]:
        """Analyze entire codebase with progress tracking"""

        files = list(Path(root_path).glob('**/*.py'))
        self.console.print(f"Found {len(files)} Python files")

        results = {}
        batches = list(chunked(files, batch_size))

        with self.console.status("Analyzing codebase...") as status:
            for i, batch in enumerate(batches):
                status.update(f"Processing batch {i+1}/{len(batches)}")

                for file in batch:
                    result = self.analyze_file(str(file))
                    results[str(file)] = result

        return results

    def _compile_patterns(self) -> Dict[str, Any]:
        """Compile analysis patterns"""
        return {
            'long_functions': lambda node: isinstance(node, ast.FunctionDef) and len(node.body) > 50,
            'deep_nesting': lambda node: isinstance(node, ast.If) and self._get_nesting_level(node) > 4,
            'unused_imports': [],  # Would be populated by import analysis
        }

    def _analyze_ast(self, tree: ast.AST, file_path: str) -> Dict[str, Any]:
        """Analyze AST tree"""
        analysis = {
            'file': file_path,
            'functions': [],
            'classes': [],
            'imports': [],
            'complexity': 0,
            'issues': []
        }

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                analysis['functions'].append(node.name)
                analysis['complexity'] += 1

            elif isinstance(node, ast.ClassDef):
                analysis['classes'].append(node.name)

            elif isinstance(node, ast.Import):
                analysis['imports'].extend(alias.name for alias in node.names)

        return analysis

    def _get_nesting_level(self, node: ast.AST) -> int:
        """Calculate nesting level of a node"""
        level = 0
        current = node
        while hasattr(current, 'orelse') and current.orelse:
            level += 1
            current = current.orelse[0] if current.orelse else None
        return level
```

## 🎯 Best Practices for Advanced Tools

1. **Use `boltons` for missing stdlib features** - `chunked()`, `cachedproperty()`
2. **Combine `funcy` + `more-itertools`** for data processing pipelines
3. **Apply `click` + `rich`** for professional CLI tools
4. **Leverage `pydantic`** for all configuration management
5. **Use `hypothesis`** for robust testing of analysis functions
6. **Implement `numba`** for performance-critical sections
7. **Apply `icecream`** for debugging instead of print statements
8. **Monitor memory with `memory_profiler`** for large analyses
9. **Use `pandas`** for statistical analysis of code metrics

## 🔄 Integration Patterns

### CLI Tool Template

```bash
# Create a new analysis command
python -m my_agent analyze ./src --output results.json --format html --verbose
```

### Configuration Management

```python
# Load config from file and environment
config = AnalysisConfig.from_env()
config.update_from_file('config.yaml')
```

### Pipeline Composition

```python
# Compose analysis pipeline
analyze_pipeline = compose(
    partial(save_results, format='json'),
    analyze_codebase,
    find_project_files
)
```

This comprehensive toolkit transforms coding agents from basic script runners into professional analysis platforms capable of handling complex refactoring, testing, and code quality assessment tasks.
