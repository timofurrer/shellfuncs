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


#: Holds the logger for shelldone
logger = logging.getLogger('shelldone')
logger.setLevel(logging.DEBUG)


class ShellScriptFinder:
    """
    Meta Path Finder to lookup
    shell scripts.
    """
    @classmethod
    def find_spec(cls, name, path=None, target=None):
        loader = ShellScriptLoader()
        spec = importlib.util.spec_from_loader(name, loader)
        spec.script = name + '.sh'
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
        if name == '__get__':  # somehow invoked by functools.partialmethod. TODO: check waht's up
            return None

        func = functools.partial(self.execute_func, name)
        return func

    def execute_func(self, name, *args):
        """
        Execute the shell function with the given name.
        """
        cmdline = '. ./{script} && {func} {args}'.format(
            script=self.script,
            func=name, args=' '.join("'{0}'".format(x) for x in args))

        proc = subprocess.Popen(cmdline, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate()
        ret = proc.wait()
        return ret, stdout, stderr


# add ShellScriptFinder as meta path finder to sys
sys.meta_path.append(ShellScriptFinder)
