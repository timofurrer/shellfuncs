"""
This module provides a Python API to shell functions coming
from a sourced shell script.

Example:

>>> import shellfuncs
>>> from my_shell_script import my_shell_func
>>> retcode, stdout, stderr = my_shell_func('Hello', 'World')
>>> print('Got return code: {0}'.format(retcode))
Got return code: 0
>>> print('Got stdout: "{0}"'.format(stdout))
Got stdout: "Hello"
>>> print('Got stderr: "{0}"'.format(stderr))
Got stderr: "World"
"""

import os
import sys
import logging
import types
import importlib.util
import subprocess
import functools
from pathlib import Path
from collections import namedtuple
from contextlib import contextmanager


#: Holds the logger for shelldone.
logger = logging.getLogger('shelldone')
logger.setLevel(logging.DEBUG)

#: Holds a type which is used as return value for executed shell functions.
ShellFuncReturn = namedtuple('ShellFuncReturn', ['returncode', 'stdout', 'stderr'])

#: Holds the configuration stack
config_stack = [
    {
        'shell': os.environ.get('SHELLFUNCS_DEFAULT_SHELL', '/bin/sh'),
        'env': os.environ
    }
]


@contextmanager
def config(shell=None, env=None):
    global config_stack

    config = config_stack[-1].copy()

    if shell is not None:
        config['shell'] = shell
    if env is not None:
        config['env'] = env

    config_stack.append(config)
    yield
    config_stack.pop()


class ShellScriptFinder:
    """
    Meta Path Finder to lookup
    shell scripts.
    """
    @classmethod
    def find_spec(cls, name, path=None, target=None):
        script_path = Path('{0}.sh'.format(name.replace('.', '/')))
        if not script_path.exists():  # no such script found.
            return None

        # TODO: check relative imports and directory walking
        loader = ShellScriptLoader()
        spec = importlib.util.spec_from_loader(name, loader)
        spec.script = script_path
        return spec


class ShellScriptLoader:
    @classmethod
    def create_module(cls, spec):
        return ShellModule(spec.name, spec.script, config_stack[-1])

    @classmethod
    def exec_module(cls, module):
        # TODO: Am I supposed to do something here?
        pass


class ShellModule(types.ModuleType):
    def __init__(self, name, script, config):
        self.script = script
        self.config = config
        super().__init__(name)

    def __getattr__(self, name):
        if name == '__get__':  # somehow invoked by functools.partialmethod. TODO: check waht's up?!
            return None

        func = functools.partial(self.execute_func, name)
        return func

    def execute_func(self, name, *args, shell=None, env=None, stdin=None, timeout=None):
        """
        Execute the shell function with the given name.
        """
        cmdline = '. ./{script} && {func} {args}'.format(
            script=str(self.script),
            func=name, args=' '.join("'{0}'".format(x) for x in args))

        shell = shell if shell else self.config['shell']
        env = env if env else self.config['env']

        proc = subprocess.Popen(cmdline, shell=True, executable=shell, env=env,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                stdin=subprocess.PIPE if stdin else None)
        stdout, stderr = proc.communicate(input=stdin, timeout=timeout)
        return ShellFuncReturn(proc.returncode, stdout, stderr)


# add ShellScriptFinder as meta path finder to sys
sys.meta_path.append(ShellScriptFinder)
