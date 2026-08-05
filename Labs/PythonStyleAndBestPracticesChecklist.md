<h1>Python Coding Style and Best Practices Checklist</h1>

<h2>For CS 212, Intro to AI Programming</h2>



### Aspects of coding style to check

- Is proper [indentation](https://peps.python.org/pep-0008/#indentation) used?

- Are variable function names descriptive and meaningful?

- Have unnecessary lines of code, commented-out code, and unused files been removed?

- Are there clear and concise comments or [docstrings](https://docs.python.org/3/glossary.html#term-docstring) explaining complex code or functions?

- Do variable, function, and method names use snake_case? 

- Are class names written using PascalCase (aka TitleCase)?

- Are constant names written using ALL_CAPS (typically defined at the module level)?

- Are import statements organized (standard library first, then third-party, then local imports)?

- Are module (file) names descriptive and written in snake_case?

### Best practices to check

- Is the code DRY (Don’t Repeat Yourself) — no duplicated logic or copy-pasted code?
- Are named constants used instead of hard-coded literal values?
- Is business logic separated from input/output code&mdash;e.g., computation in one module (file), CLI handling in another?
- Are local variables used inside methods whenever possible, instead of storing data in [class or instance attributes (variables)](https://docs.python.org/3/tutorial/classes.html#class-and-instance-variables) unnecessarily?
- Are instance variables intended for internal use prefixed with an underscore (e.g., _value)?
- Does each function or method do one clear task and have a single responsibility (no “Swiss Armey” methods)?
- Are classes cohesive (each has a clear, well-defined purpose) and loosely coupled (minimal dependencies on other classes)
- Is inheritance used appropriately, or replaced with composition where simpler?
- Are [data classes](https://docs.python.org/3/library/dataclasses.html) (@dataclass) used where appropriate for simple data containers?



For the full Python style guide see the [official PEP-8 web page](https://peps.python.org/pep-0008/).

---



[![Creative Commons License](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-sa/4.0/) Intro to AI Programming Course Materials by [Brian Bird](https://profbird.dev), written in <time>2025</time>, are licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/). 

---
