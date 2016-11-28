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

import sys
import logging
import types
import importlib.util
import subprocess
import functools
from pathlib import Path
from collections import namedtuple


#: Holds the logger for shelldone.
logger = logging.getLogger('shelldone')
logger.setLevel(logging.DEBUG)

#: Holds a type which is used as return value for executed shell functions.
ShellFuncReturn = namedtuple('ShellFuncReturn', ['returncode', 'stdout', 'stderr'])


class ShellScriptFinder:
    """
    Meta Path Finder to lookup
    shell scripts.
    """
    @classmethod
    def find_spec(cls, name, path=None, target=None):
        script_path = Path('{0}.sh'.format(name))
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
        return ShellModule(spec.name, spec.script)

    @classmethod
    def exec_module(cls, module):
        # TODO: Am I supposed to do something here?
        pass


class ShellModule(types.ModuleType):
    def __init__(self, name, script):
        self.script = script
        super().__init__(name)

    def __getattr__(self, name):
        if name == '__get__':  # somehow invoked by functools.partialmethod. TODO: check waht's up?!
            return None

        func = functools.partial(self.execute_func, name)
        return func

    def execute_func(self, name, *args):
        """
        Execute the shell function with the given name.
        """
        # TODO: allow to specify which shell is used
        # TODO: allow to specify environment which is used
        cmdline = '. ./{script} && {func} {args}'.format(
            script=str(self.script),
            func=name, args=' '.join("'{0}'".format(x) for x in args))

        proc = subprocess.Popen(cmdline, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate()
        return ShellFuncReturn(proc.returncode, stdout, stderr)


# add ShellScriptFinder as meta path finder to sys
sys.meta_path.append(ShellScriptFinder)
