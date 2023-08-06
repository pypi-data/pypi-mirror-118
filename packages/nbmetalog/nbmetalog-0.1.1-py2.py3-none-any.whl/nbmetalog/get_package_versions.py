import inspect
import types

from . import _except_return_none

def _do_get_package_versions(stack_idx):

    caller_globals = inspect.stack()[stack_idx][0].f_globals

    caller_base_module_names = [
        val.__name__.split('.')[0]
        for val in caller_globals.values()
        if isinstance(val, types.ModuleType)
    ] + [
        'IPython',
    ]

    res = {}

    for base_module in sorted(caller_base_module_names):
        exec(f'import {base_module}', globals())
        exec(
            f'version = getattr({base_module}, "__version__", None)',
            globals(),
        )
        if version:
            res[base_module] = version

    return res


@_except_return_none
def get_package_versions():

    stack_len = len(inspect.stack())
    return {
        k : v
        for stack_idx in range(stack_len)
        for k, v in _do_get_package_versions(stack_idx).items()
    }
