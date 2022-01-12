# Janus

[![Build Status](https://github.com/usharerose/janus/actions/workflows/ci.yaml/badge.svg)](https://github.com/usharerose/janus/actions/workflows/ci.yaml)

An analyzer of code cyclomatic complexity, which only works with Python 3.

A list of supported languages:

* Python
* Golang

## Installation

```sh
pip3 install git+https://github.com/usharerose/janus.git
```

## Usage

### Command Line

```sh
Usage: janus [OPTIONS] [PATHS]...

  Args:     paths (tuple): the paths of files or directories

Options:
  --help  Show this message and exit.
```

You can input a file as target
```sh
janus foo.py
```

You can input directory, and analyze the files under it recursively
```sh
janus directory/
```

You can also input multiple paths
```sh
janus directory/ foo.py
```

### Python Module

```python
>>> from janus.app import Janus
>>> app = Janus()
>>> result = app.process(('/foo.py',))
>>> print(result)
{"data": [{"file": "/foo.py", "cyclomatic_complexity": 27}]}
```

## Theory

According to the definition of `cyclomatic complexity` in [Wikipedia](https://en.wikipedia.org/wiki/Cyclomatic_complexity)

> Cyclomatic complexity is a software metric used to indicate the complexity of a program. It is a quantitative measure of the number of linearly independent paths through a program's source code. It was developed by Thomas J. McCabe, Sr. in 1976.

The library is based on the following formula

```
V(G) = P + 1

* P is the number of decision points in the program
```

## Development

### Support New Language

1. Add the language-specific `tree-sitter` as submodule
```
[submodule "vendor/tree-sitter-go"]
	path = vendor/tree-sitter-go
	url = https://github.com/tree-sitter/tree-sitter-go
```

2. Execute the script to store the multiple `tree-sitter` into the library for local dev
```sh
python build_tree_sitter_lang_lib.py
```

3. Register the mapping of language's file extension to name in the file `janus/settings.py`
```python
EXTENSION_LANG_NAME_MAPPING = {
    '.py': 'python',
    '.go': 'go',
    # please add it here
}
```

4. Add the language-specific analyzer into the file `janus/analyzer.py` inherited from `BaseComplexityAnalyzer`. Commonly you only need to overwrite the following configurations
```python
class FooAnalyzer(BaseComplexityAnalyzer):

    EXTENSION = '.foo'

    # refer to the value in https://github.com/tree-sitter/tree-sitter-foo/blob/master/src/grammar.json
    DECISION_TYPES = [
        'if', ...
    ]
```

5. Add test cases under the directory `tests/`
