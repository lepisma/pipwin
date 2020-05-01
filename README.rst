===============================
pipwin
===============================


.. image:: https://img.shields.io/pypi/v/pipwin.svg?style=flat-square
    :target: https://pypi.python.org/pypi/pipwin/
    :alt: Latest Version

.. image:: https://img.shields.io/appveyor/ci/lepisma/pipwin.svg?style=flat-square
    :target: https://ci.appveyor.com/project/lepisma/pipwin
    :alt: Build

.. image:: https://img.shields.io/pypi/l/pipwin.svg?style=flat-square
    :target: https://pypi.python.org/pypi/pipwin/
    :alt: License

**pipwin** is a complementary tool for **pip** on Windows. **pipwin** installs
unofficial python package binaries for windows provided by Christoph Gohlke here
`http://www.lfd.uci.edu/~gohlke/pythonlibs/
<http://www.lfd.uci.edu/~gohlke/pythonlibs/>`_

**Version 0.2.X changes the structure of cache file. Make sure to run `pipwin refresh` if updated.**

QuickStart
^^^^^^^^^^

.. code-block::

   >> pip install pipwin
   >> pipwin search cv

   Did you mean any of these ?

     * cvxopt
     * opencv-python
     * abcview
     * cvxpy

   >> pipwin install opencv-python

   >> pipwin install numpy>=1.11


Details
^^^^^^^

- On first run, **pipwin** builds a cache of available package list in ``~/.pipwin``

- You can force a cache rebuild using : ``pipwin refresh``

- List all available packages : ``pipwin list``

- Search packages : ``pipwin search <partial_name/name>``

- Install packages : ``pipwin install <package>``

  Also works version specifiers, e.g. ``pipwin install <package>==<version>`` or
  ``pipwin install <package><=<version>``

- Download only (to ``~/pipwin`` or ``<dest>`` if provided) : ``pipwin
  download -d <dest> <package>``

- Install from pipwin requirements file : ``pipwin install -r requirements.txt``

- Download only from pipwin requirements file : ``pipwin download -r
  requirements.txt``

- Uninstall packages (Can directly use **pip** for this) : ``pipwin uninstall
  <package>``

**Free software: BSD license**


Changelog
---------

v0.5.0
~~~~~~

- Handles text vs string parsing for beautifulsoup4 for python2 vs python3.
- Fixes [issue 43](https://github.com/lepisma/pipwin/issues/43)

v0.4.9
~~~~~~

- More robust whitespace handling in requirement parsing.

v0.4.8
~~~~~~

- Using PySmartDL to handle download and install of packages.
- Removed progress bar and streaming downloader blocks now handled by PySmartDL.

v0.4.7
~~~~~~

- Using postman client type to overcome use of robobrowser to create package
  cache.
