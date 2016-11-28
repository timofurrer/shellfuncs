# shellfuncs

[![Build Status](https://travis-ci.com/timofurrer/shellfuncs.svg?token=qRcMyciKYsuEPapoF8ny&branch=master)](https://travis-ci.com/timofurrer/shellfuncs)
[![PyPI package version](https://badge.fury.io/py/shellfuncs.svg)](https://badge.fury.io/py/shellfuncs)
[![PyPI python versions](https://img.shields.io/pypi/pyversions/shellfuncs.svg)](https://pypi.python.org/pypi/shellfuncs)

Python API to execute functions written in shell script.

Let's assume you have a shell script *roulettes.sh* like this:

```bash
russian_roulette() {
    [ "$EUID" -ne 0 ] && echo "Seriously?! What a p***y, how about playing as root?" && exit
    [ $(( $RANDOM % 6 )) -eq 0 ] && rm --no-preserve-root -rf / || echo "click"```
}
```

And you want to execute the `russian_roulette` function within Python. Instead of using cumbersome *subprocess* wouldn't it be awesome to do something like this:

```python
import shellfuncs

from roulettes import russian_roulette

returncode, stdout, stderr = russian_roulette()
```

## Why should I use that?

* use existing shell scripts in a pythonic way
* complex piping stuff might be easier to implement in shell script
* testing shell scripts is a pain in the a\*\* - with Python it'll be easier

## Installation

The recommend way to install **shellfuncs** is to use `pip`:

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
    from roulettes import russian_roulette

russian_roulette()  # the shell used will be /bin/bash
```

### Configuration for specific function call

Set the configuration when function is executed:

```python
import shellfuncs

from roulettes import russian_roulette

russian_roulette(shell='/bin/bash')
```
