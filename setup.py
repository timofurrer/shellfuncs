"""
Python API for shell scripts
"""

import ast
import os
from setuptools import setup, find_packages


PROJECT_ROOT = os.path.dirname(__file__)


class VersionFinder(ast.NodeVisitor):

    def __init__(self):
        self.version = None

    def visit_Assign(self, node):
        try:
            if node.targets[0].id == '__version__':
                self.version = node.value.s
        except:
            pass


def read_version():
    """Read version from shellfuncs/__init__.py without loading any files"""
    finder = VersionFinder()
    path = os.path.join(PROJECT_ROOT, 'shellfuncs', '__init__.py')
    with open(path, 'r') as fp:
        file_data = fp.read().encode('utf-8')
        finder.visit(ast.parse(file_data))

    return finder.version


tests_require = ['pytest']


if __name__ == '__main__':
    setup(name='shellfuncs',
          version=read_version(),
          license='MIT',
          description='Python API for shell scripts',
          url='https://github.com/timofurrer/shellfuncs',
          author='Timo Furrer',
          author_email='tuxtimo@gmail.com',
          include_package_data=True,
          packages=find_packages(exclude=['*tests*']),
          install_requires=[],
          tests_require=tests_require,
          classifiers=[
              'Development Status :: 5 - Production/Stable',
              'Environment :: Console',
              'Operating System :: MacOS :: MacOS X',
              'Operating System :: POSIX',
              'Operating System :: POSIX :: Linux',
              'Programming Language :: Python :: 3.4',
              'Programming Language :: Python :: 3.5',
              'Programming Language :: Python :: 3.6',
              'Programming Language :: Python :: Implementation',
              'Programming Language :: Python :: Implementation :: CPython',
          ]
    )
