============
nbmetalog
============


.. image:: https://img.shields.io/pypi/v/nbmetalog.svg
        :target: https://pypi.python.org/pypi/nbmetalog

.. image:: https://img.shields.io/travis/mmore500/nbmetalog.svg
        :target: https://travis-ci.com/mmore500/nbmetalog

.. image:: https://readthedocs.org/projects/nbmetalog/badge/?version=latest
        :target: https://nbmetalog.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




nbmetalog helps you log jupyter notebook metadata


* Free software: MIT license
* Documentation: https://nbmetalog.readthedocs.io.


.. code-block:: python3

  from nbmetalog import nbmetalog as nbm

  # prints metadata about notebook runtime
  nbm.print_metadata()

  # returns a dict with notebook metadata
  nbm.collate_summary_metadata()


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
