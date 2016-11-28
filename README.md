# shellfuncs

[![Build Status](https://travis-ci.com/timofurrer/shellfuncs.svg?token=qRcMyciKYsuEPapoF8ny&branch=master)](https://travis-ci.com/timofurrer/shellfuncs)

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
