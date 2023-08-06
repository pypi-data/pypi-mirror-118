import ipynbname
import os

from . import _except_return_none

@_except_return_none
def get_notebook_name():
    try:
        return ipynbname.name()
    except:
        return str(
            os.getenv('NOTEBOOK_NAME')
        )
