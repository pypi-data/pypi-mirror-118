"""Main module."""

from keyname import keyname as kn
import yaml

from . import get_env_context
from . import get_git_revision
from . import get_hostname
from . import get_interpreter
from . import get_notebook_cell_execution_count
from . import get_notebook_name
from . import get_notebook_path
from . import get_package_versions
from . import get_session_uuid
from . import get_timestamp

def collate_summary_metadata():
    return {
        'context' : get_env_context(),
        'nbcellexec' : get_notebook_cell_execution_count(),
        'nbname' : get_notebook_name(),
        'nbpath' : get_notebook_path(),
        'revision' : get_git_revision(),
        'session' : get_session_uuid(),
        'timestamp' : get_timestamp(),
    }

def collate_outattr_metadata():
    return {
        '_' + k : kn.demote(v) if v is not None else None
        for k, v in collate_summary_metadata().items()
    }

def collate_full_metadata():
    return {
        'context' : get_env_context(),
        'hostname' : get_hostname(),
        'interpreter' : get_interpreter(),
        'nbcellexec' : get_notebook_cell_execution_count(),
        'nbname' : get_notebook_name(),
        'nbpath' : get_notebook_path(),
        'revision' : get_git_revision(),
        'session' : get_session_uuid(),
        'timestamp' : get_timestamp(),
    }


def print_metadata():

    print(
        yaml.dump( collate_full_metadata() )
    )

    print()

    for k, v in get_package_versions().items():
        print(f'{k}=={v}')
