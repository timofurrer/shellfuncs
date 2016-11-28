"""
Test shellfuncs
"""

import shellfuncs

def test_basic_import():
    """
    Test basic import functionality
    """
    from .input_scripts.foo import bar

    returncode, stdout, stderr = bar('STDOUT', 'STDERR')

    assert returncode == 0
    assert stdout == b'STDOUT\n'
    assert stderr == b'STDERR\n'


def test_shell_config():
    """
    Test configuring shell
    """
    with shellfuncs.config(shell='/bin/bash'):
        from .input_scripts.config import used_shell

    _, stdout, _ = used_shell()
    assert stdout == b'/bin/bash\n'

    _, stdout, _ = used_shell(shell='/bin/sh')
    assert stdout == b'/bin/sh\n'
