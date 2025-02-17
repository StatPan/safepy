# reop

**reop** is a lightweight Python library inspired by Rust's `Result` and `Option` patterns. The name combines **"Result"** and **"Option"**, representing the two core concepts of the library.

## Why Use reop?
### The Problem
Python's try/except for error handling and the frequent use of None as a placeholder for missing values are flexible, but they often lack clarity:

**Implicit failures**: A function might fail, but this is not explicit in its return type.
Unclear intent: None values can propagate silently, making debugging harder.
Ad-hoc error handling: Handling errors consistently across large codebases is challenging.
## The Solution
With reop, you can leverage Rust-inspired patterns for safer and clearer error handling:

**Explicit Error Handling**:
Functions return Result[ValueType, ErrorType] to indicate success or failure explicitly.
No unexpected exceptions—errors are part of the function's return type.
Structured Value Management:
Use Option to represent values that may or may not exist.
No more unchecked None values—intent is always explicit.
Composable and Readable Code:
Chain operations on Result and Option objects with methods like map, and_then, and or_else.

## Installation

```bash
pip install reop
```

## Usage
Using Result for Explicit Error Handling
```python
from reop import Result, result_wrapper

@result_wrapper
def divide(a: int, b: int) -> float:
    return a / b

# Example 1: Successful division
result = divide(10, 2)
if result.is_ok:
    print(f"Success: {result.unwrap()}")  # Output: Success: 5.0

# Example 2: Division by zero
result = divide(10, 0)
if result.is_err:
    print(f"Error: {result.unwrap_err()}")  # Output: Error: division by zero

```

Using Option for Optional Values
```python
from reop import Option, option_wrapper

@option_wrapper
def find_value(key: str, data: dict) -> Optional[int]:
    return data.get(key)

# Example 1: Key exists
option = find_value("a", {"a": 42})
if option.is_some:
    print(f"Found: {option.unwrap()}")  # Output: Found: 42

# Example 2: Key does not exist
option = find_value("b", {"a": 42})
print(option.unwrap_or(0))  # Output: 0

```

## Key Benefits of reop
Improved Clarity: Make function intentions and possible failure cases explicit.
Safer Code: Avoid unexpected None values or unhandled exceptions.
Rust-inspired: Adopt proven patterns from Rust for Python programming.
Composable Methods: Chain operations for clean and concise workflows.
