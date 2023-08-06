from functools import lru_cache
import pathlib
import subprocess

from . import _except_return_none

@lru_cache()
@_except_return_none
def get_git_revision():
    return subprocess.check_output([
        'git',
        '-C',
        pathlib.Path(__file__).parent.absolute(),
        'rev-parse',
        '--short',
        'HEAD',
    ]).decode('ascii').strip()
