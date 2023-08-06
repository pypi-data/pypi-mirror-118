import os

from . import _except_return_none

@_except_return_none
def get_env_context():
    return 'ci' if os.getenv('CI') else 'local'
