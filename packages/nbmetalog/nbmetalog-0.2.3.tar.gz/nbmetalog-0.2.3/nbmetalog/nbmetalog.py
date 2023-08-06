"""Main module."""

import hurry.filesize as hurry
from keyname import keyname as kn
import yaml

from . import get_dataframe_full_digest
from . import get_dataframe_manifest
from . import get_dataframe_short_digest
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

def collate_dataframe_summary(df, name=None):
    if name is not None:
        return {
            **{
                'a' : name
            },
            **collate_dataframe_summary(df)
        }
    else:
        return {
            'digest' : get_dataframe_full_digest(df),
            'num cols' : len(df.columns),
            'num cols any na' : len(df.columns[df.isnull().any()]),
            'num cols all na' : len(df.columns[df.isnull().all()]),
            'num na' : int(df.isnull().sum().sum()),
            'num rows' : len(df.index),
            'num rows any na' : int(df.isnull().any(axis=1).sum()),
            'num rows all na' : int(df.isnull().all(axis=1).sum()),
            'size' : hurry.size(df.memory_usage(deep=True).sum()),
        }

def collate_dataframe_synopsis(*args):
    return {
        **{
            'manifest' : get_dataframe_manifest(args[0]),
        },
        **collate_dataframe_summary(*args)
    }


def print_dataframe_manifest(df):
    print(
        yaml.dump( get_dataframe_manifest( df ) )
    )

def print_dataframe_summary(*args):
    print(
        yaml.dump( collate_dataframe_summary( *args ) )
    )

def print_dataframe_synopsis(*args):
    print(
        yaml.dump( collate_dataframe_synopsis( *args ) )
    )

def nvp_expr(varname):
    return '{0}, "{0}"'.format(varname)
