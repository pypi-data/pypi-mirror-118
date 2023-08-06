import ipynbname
import os

from . import _except_return_none

@_except_return_none
def get_notebook_path():
    try:
        return str(
            ipynbname.path()
        )
    except:
        return str(
            os.getenv('NOTEBOOK_PATH')
        )
