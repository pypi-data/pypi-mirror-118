"""Top-level package for nbmetalog."""

__author__ = """Matthew Andres Moreno"""
__email__ = 'm.more500@gmail.com'
__version__ = '0.1.1'

from ._except_return_none import _except_return_none
from .get_env_context import get_env_context
from .get_git_revision import get_git_revision
from .get_hostname import get_hostname
from .get_interpreter import get_interpreter
from .get_notebook_cell_execution_count import get_notebook_cell_execution_count
from .get_notebook_name import get_notebook_name
from .get_notebook_path import get_notebook_path
from .get_package_versions import get_package_versions
from .get_session_uuid import get_session_uuid
from .get_timestamp import get_timestamp
