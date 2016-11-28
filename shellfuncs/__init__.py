"""
This module provides a Python API to shell functions coming
from a sourced shell script.
"""

from .core import config

__version__ = '0.1.0'

# Expose only specific stuff
__all__ = ['config']
