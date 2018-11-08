Using Sphinx for Documentation
==============================

`Sphinx <http://www.sphinx-doc.org/en/stable/index.html>`_ provides tools for building documentation for Python projects - and other things.

Installation Guide
------------------

Usually::

  pip install sphinx

See `the installation guide
<http://www.sphinx-doc.org/en/stable/usage/installation.html>`_ for
more details.


A Toy Project
-------------

Create a simple Python module like ``temp.py``. Save it into a
directory, create a ``docs`` directory, change there and run::

  sphinx-quickstart

This will build all the infrastructure necessary for Sphinx. In order
to build the documentation as a series of html files use::

  make clean html

The documentation will be built in the ``_build/html`` directory of
your ``docs``; you can open ``index.html`` with your web browser.

Adding the API
~~~~~~~~~~~~~~

In order to add ``temp.py`` to the documentation, you have to tell
Sphinx where it is. Comment out the part in the top of ``conf.py`` so
that it looks like this::

  import os
  import sys
  sys.path.insert(0, os.path.abspath('..'))

Now create a file ``api.rst`` in the ``docs`` directory, which
contains the following lines::
  
  API
  ===
  .. automodule:: temp
     :members:

and add ``api`` to the table of contents in your ``index.rst``::

  .. toctree::
     :maxdepth: 2

     api 

Rebuild your documentation with ``make clean html``. The API is now listed.

Publishing the Documentation on readthedocs.org
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In order to publish your documentation, your project has to be a
github repository.

Create an account for `readthedocs.org <https://readthedocs.org/>`_,
link it with your github account, and hit ``Import a Project`` on your
dashboard. Select your repository, give it a unique name, and that's
it: your documentation is online and will be updated with every pull
request or merge.


