|PyPI version| |DOI| |Total alerts| |Language grade: Python|
|numpy-eiei|

numpy-eiei : Equilibrated Input Embedding Initialization (EIEI)
===============================================================

EIEI is a procedure to initialize the weights of an input embedding.

Usage
-----

.. code:: py

   # Load some data
   corpus = """Lorem ipsum dolor sit amet, ..."""

   # Build a token list
   import kshingle as ks
   tokens = [c for c in corpus]
   TOKENLIST = list(set(tokens))
   TOKENLIST.append("[UNK]")
   TOKENLIST.append("[MASK]")
   tokenlist_size = len(TOKENLIST)
   encoded = ks.encode_with_vocab(tokens, TOKENLIST, tokenlist_size - 2)

   # Initialize the Embedding with the EIEI algorithm
   from numpy_eiei import eiei
   emb = eiei(
       encoded,
       tokenlist_size,
       embed_dim=300,
       max_context_size=14,
       max_patience=6,
       pct_add=0.1,
       fill=False
   )

Appendix
--------

Installation
~~~~~~~~~~~~

The ``numpy-eiei`` `git repo <http://github.com/ulf1/numpy-eiei>`__ is
available as `PyPi package <https://pypi.org/project/numpy-eiei>`__

.. code:: sh

   pip install numpy-eiei
   pip install git+ssh://git@github.com/ulf1/numpy-eiei.git

Install a virtual environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: sh

   python3 -m venv .venv
   source .venv/bin/activate
   pip install --upgrade pip
   pip install -r requirements.txt --no-cache-dir
   pip install -r requirements-dev.txt --no-cache-dir
   pip install -r requirements-demo.txt --no-cache-dir

(If your git repo is stored in a folder with whitespaces, then don’t use
the subfolder ``.venv``. Use an absolute path without whitespaces.)

Python commands
~~~~~~~~~~~~~~~

-  Jupyter for the examples: ``jupyter lab``
-  Check syntax:
   ``flake8 --ignore=F401 --exclude=$(grep -v '^#' .gitignore | xargs | sed -e 's/ /,/g')``
-  Run Unit Tests: ``PYTHONPATH=. pytest``

Publish

.. code:: sh

   pandoc README.md --from markdown --to rst -s -o README.rst
   python setup.py sdist
   twine upload -r pypi dist/*

Clean up
~~~~~~~~

.. code:: sh

   find . -type f -name "*.pyc" | xargs rm
   find . -type d -name "__pycache__" | xargs rm -r
   rm -r .pytest_cache
   rm -r .venv

Support
~~~~~~~

Please `open an issue <https://github.com/ulf1/numpy-eiei/issues/new>`__
for support.

Contributing
~~~~~~~~~~~~

Please contribute using `Github
Flow <https://guides.github.com/introduction/flow/>`__. Create a branch,
add commits, and `open a pull
request <https://github.com/ulf1/numpy-eiei/compare/>`__.

.. |PyPI version| image:: https://badge.fury.io/py/numpy-eiei.svg
   :target: https://badge.fury.io/py/numpy-eiei
.. |DOI| image:: https://zenodo.org/badge/DOI/10.5281/zenodo.4284804.svg
   :target: https://doi.org/10.5281/zenodo.4284804
.. |Total alerts| image:: https://img.shields.io/lgtm/alerts/g/ulf1/numpy-eiei.svg?logo=lgtm&logoWidth=18
   :target: https://lgtm.com/projects/g/ulf1/numpy-eiei/alerts/
.. |Language grade: Python| image:: https://img.shields.io/lgtm/grade/python/g/ulf1/numpy-eiei.svg?logo=lgtm&logoWidth=18
   :target: https://lgtm.com/projects/g/ulf1/numpy-eiei/context:python
.. |numpy-eiei| image:: https://snyk.io/advisor/python/numpy-eiei/badge.svg
   :target: https://snyk.io/advisor/python/numpy-eiei
