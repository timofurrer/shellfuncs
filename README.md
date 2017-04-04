# shellfuncs

[![Build Status](https://travis-ci.com/timofurrer/shellfuncs.svg?token=qRcMyciKYsuEPapoF8ny&branch=master)](https://travis-ci.com/timofurrer/shellfuncs)
[![PyPI package version](https://badge.fury.io/py/shellfuncs.svg)](https://badge.fury.io/py/shellfuncs)
[![PyPI python versions](https://img.shields.io/pypi/pyversions/shellfuncs.svg)](https://pypi.python.org/pypi/shellfuncs)

Python API to execute functions written in shell script.

Let's assume you have a shell script *counters.sh* like this:

```bash
count_python_imports() {
    find -name '*.py' | xargs grep -e '^import os$' -e '^import sys$' -e '^import re$' | cut -d: -f2 | sort | uniq -c
}
```

And you want to execute the `count_python_imports` function within Python. Instead of using cumbersome *subprocess* wouldn't it be awesome to do something like this:

```python
import shellfuncs

from counters import count_python_imports

returncode, stdout, stderr = count_python_imports()
```

*Yeah, yeah, I know about easier ways of achieving the above, too. Thanks.*

## Why should I use that?

* use existing shell scripts in a pythonic way
* complex piping stuff might be easier to implement in shell script
* testing shell scripts is a pain in the a\*\* - with Python it'll be easier

## Installation

The recommended way to install **shellfuncs** is to use `pip`:

```shell
pip install shellfuncs
```

## Usage

**shellfuncs** can be configured on different levels.

The following configuration variables are available:

* shell (defaults to `/bin/sh`)
* env (defaults to `os.environ`)

### Configuration via environment variables

Set the default shell via `SHELLFUNCS_DEFAULT_SHELL` environment variable:

```bash
export SHELLFUNCS_DEFAULT_SHELL=/bin/bash
```

### Configuration via context manager

Set the configuration block-wise with a context manager:

```python
import shellfuncs

with shellfuncs.config(shell='/bin/bash'):
    from counters import count_python_imports

count_python_imports()  # the shell used will be /bin/bash
```

### Configuration for specific function call

Set the configuration when function is executed:

```python
import shellfuncs

from counters import count_python_imports

count_python_imports(shell='/bin/bash')
```

***

*<p align="center">This project is published under [MIT](LICENSE).<br>A [Timo Furrer](https://tuxtimo.me) project.<br>- :tada: -</p>*
