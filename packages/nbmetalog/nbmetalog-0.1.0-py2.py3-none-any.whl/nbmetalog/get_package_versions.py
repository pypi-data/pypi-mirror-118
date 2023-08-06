import inspect
import types

from . import _except_return_none

@_except_return_none
def get_package_versions():

    caller_globals = inspect.stack()[1][0].f_globals

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
