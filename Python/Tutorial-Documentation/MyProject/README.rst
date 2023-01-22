================================================================================
Tutorial-Documentation
================================================================================

This package provides simple examples of the python documentation system.

The python documentation system includes the PEP standards for docstrings as well as the tools for automatically generating documentation such as Sphinx and PyDoc



Setup
------------

.. code-block:: bash

    $ conda install --file requirements.txt

PyDoc
---------------------------

`pydoc <https://docs.python.org/3/library/pydoc.html>`_ is mostly identical to
calling ``help()`` from within a python interactive session. However, there are
two main differences. The first is a small benefit, namely that ``pydoc`` can be
called from the command line and therefore doesn't require importing packages
first.

.. code-block:: bash

    $ pydoc mypackage/myclass.py

The second is that pydoc can generate HTML pages.
Running

.. code-block:: bash

    $ pydoc -b

will start an HTTP server on an arbitrary unused port and open a Web browser to
interactively browse the documentation.

To generate an HTML file for a single module, run

.. code-block:: bash

    $ pydoc -w mypackage/myclass.py

PyDoc is useful for quick surveys of documentation and for generating informal
documentation of a single module. For larger and more public projects, Sphinx is
recommended.

Sphinx
---------------------------

`Sphinx <https://www.sphinx-doc.org/en/master/index.html>`_ is the documentation tool of choice for most major projects.


Initial Setup
^^^^^^^^^^^^^

.. code-block:: bash

    $ cd MyProject/docs
    $ sphinx-quickstart
    # > Separate source and build directories (y/n) [n]: y
    # > Project name: MyProject
    # > Author name(s): Alex Armstrong
    # > Project release []: 0.0.1
    # > Project language [en]: en

Edit the ``source/conf.py`` file to include the project path

.. code-block:: py

    import os
    import sys
    sys.path.insert(0, os.path.abspath('../..'))

and to add these extensions

.. code-block:: py

    extensions = [
             'sphinx.ext.autodoc',
             'sphinx.ext.napoleon',
             'sphinx.ext.todo'
    ]

Automatically generate the needed source files

.. code-block:: bash

    $ sphinx-apidoc -f -o source/ ../

Edit the ``source/index.rst`` file to point it correct files:

.. code-block:: rst

    .. toctree::
       :maxdepth: 2
       :caption: Contents:

       modules.rst

Generate documentation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    $ sphinx-build -b html source/ build/

or, from inside ``docs/``, simply run

.. code-block:: bash

    $ make html

The main html page can then be opened with

.. code-block:: bash

    $ open build/html/index.html

References
----------
* Generally useful articles
    * `Documenting Python Code: A Complete Guide <https://realpython.com/documenting-python-code/>`_ by James Mertz on Real Python
    * `Stack Overflow - "What is the standard Python docstring format?" <https://stackoverflow.com/questions/3898572/what-is-the-standard-python-docstring-format>`_ - a good summary of ReST, Google, Numpydoc, and other docstring flavors
* Documentation PEPs
    * `PEP 8 -- Style Guide for Python Code <https://www.python.org/dev/peps/pep-0008/>`_
    * `PEP 257 -- Docstring Conventions <https://www.python.org/dev/peps/pep-0257/>`_
    * `PEP 287 -- reStructuredText Docstring Format <https://www.python.org/dev/peps/pep-0287/>`_
    * `PEP 484 -- Type Hints <https://www.python.org/dev/peps/pep-0484/>`_
    * `PEP 526 -- Syntax for Variable Annotations <https://www.python.org/dev/peps/pep-0526/>`_
* Sphinx
    * `Sphinx Home Page <https://www.sphinx-doc.org/en/master/index.html>`_
        * `sphinx.ext.napoleon <http://man.hubwiz.com/docset/Sphinx.docset/Contents/Resources/Documents/latest/ext/napoleon.html>`_
    * `"An idiot's guide to Python documentation with Sphinx and ReadTheDocs" <https://samnicholls.net/2016/06/15/how-to-sphinx-readthedocs/>`_ by Sam Nicholls
* reStructuredText
    * `Online Sphinx Editor <https://livesphinx.herokuapp.com/>`_
    * `Online RST Editor <http://rst.ninjs.org/>`_ - Less helpful display but can convert to PDF
    * `Sphinx RST guide <https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html>`_
    * `Official User Guide <https://docutils.sourceforge.io/rst.html>`_ - Examples don't display final output
