PEP: XXX
Title: Distributing a Subset of the Standard Library
Version: $Revision$
Last-Modified: $Date$
Author: Tomáš Orsava <torsava@redhat.com>,
        Petr Viktorin <pviktori@redhat.com>
Status: Draft
Type: Standards Track
Content-Type: text/x-rst
Created: 5-Sep-2016
Python-Version: 3.6
Post-History: 

.. warning::
    TODO
    1. Don't forget 2 spaces after every sentence (Python developers should really read a manual of style).
    2. Text should be longer than 70 but no longer than 79 characters.

Abstract
========

.. XXX::

    Write this last :)

    (~200 words)

    This PEP should handle step ``1)`` from the initial discussion (link?).

Motivation
==========
.. The motivation is critical for PEPs that want to change the Python language.  It should clearly explain why the existing language specification is inadequate to address the problem that the PEP solves.  PEP submissions without sufficient motivation may be rejected outright.

There are several use cases for including only a subset of Python's standard library.  For example, when a *stdlib* module with missing dependencies is skipped during the Python build process.  For another, a considerable amount of space can be saved by not distributing irrelevant parts of the standard library, such as ``TkInter`` on headless servers.

However, there is so far no formal specification of how to properly implement distribution of a subset of the standard library.  Namely, how to safely handle attempts to import a missing *stdlib* module, and display an informative error message.


CPython
-------
When one of Python standard library modules (such as ``_sqlite3``) cannot be compiled during a Python build because of missing dependencies (e.g. SQLite header files), the module is simply skipped.

If you then install this compiled Python and use it to try to import one of the missing modules, Python will go through the ``sys.path`` entries looking for it.  It won't find it among the *stdlib* modules and thus it will continue onto ``site-packages`` and fail with an ``ImportError`` if it doesn't find it.

This can confuse users who may not understand why a cleanly build Python is missing standard library modules.  In addition it introduces a possible security issue: ``site-packages`` can contain broken or even malicious code that may be, unbeknownst to the user, imported instead of the missing *stdlib* module.


Linux and other distributions
-----------------------------
Many Linux and other distributions are already separating out parts of the standard library to standalone packages.  Among the most commonly excluded modules are the ``TkInter`` module, since it draws in a dependency on the graphical environment, and the ``test`` module, as it only serves to test Python internally and is about as big as the rest of the standard library put together.

The methods of omission of these modules differ.  For example, Debian patches the file ``Lib/tkinter/__init__.py`` to envelop the line ``import _tkinter`` in a *try-except* block and upon encountering an ``ImportError`` it simply adds the following to the error message: ``please install the python3-tk package`` [#debian-patch]_.  Fedora and other distributions simply don't include the omitted modules, potentially leaving users baffled as to where to find them.

In addition, both these methods also introduce the aforementioned security issue of possibly importing an insecure ``site-packages`` module in lieu of the missing *stdlib* module.


Specification
=============
.. The technical specification should describe the syntax and semantics of any new language feature.  The specification should be detailed enough to allow competing, interoperable implementations for at least the current major Python platforms (CPython, Jython, IronPython, PyPy).

When, for any reason, a standard library module is not to be included with the rest, a file with it's name and an extension ``.missing.py`` should be created and placed in the *stdlib* directory or any other location on ``sys.path`` the module would have occupied.

When Python tries to import a module ``XYZ``, it goes through the entries in ``sys.path`` and in each location looks for a file whose name is ``XYZ`` with one of the valid Python extensions (``.*.so``, ``.so``, ``.py``, ``.*.pyc``, ``.pyc``).  If none of them are found in the currently searched location, Python will now continue by looking for a file named ``XYZ.missing.py`` in the same location, and import it if found.  Due to looking for the ``.missing.py`` file last in each ``sys.path`` location, the missing file will never shadow an actually installed module in any given location.

The file with the ``.missing.py`` extension can contain anything the distributor wishes, however, it *should* raise an ``ImportError`` with a helpful error message.


Rationale
=========
.. The rationale fleshes out the specification by describing what motivated the design and why particular design decisions were made.  It should describe alternate designs that were considered and related work, e.g. how the feature is supported in other languages.
   The rationale should provide evidence of consensus within the community and discuss important objections or concerns raised during discussion.

The mechanism of handling missing standard library modules through the use of the ``.missing.py`` files was chosen due to its advantages both for CPython itself and for Linux and other distributions that are packaging it.

First, this implementation solves the security issue of importing, unbeknownst to the user, a possibly insecure module from ``site-packages`` instead of the missing standard library module.  Now, Python will import the ``.missing.py`` file and won't ever look for a *stdlib* module in ``site-packages``.

Another advantage is that the standard library module can be subsequently installed simply by putting the module file in it's appropriate location, which will then take precedence over the corresponding ``.missing.py`` file.

In addition, this method of handling missing *stdlib* modules can be implemented in a succinct, non-intrusive way in CPython, and thus won't add to the complexity of the existing code base.

Lastly, due to the nature of handling missing *stdlib* modules through the use of separate ``.missing.py`` files, the content of the file can be customized by the packager to provide any desirable behaviour.  Beginning with providing a tailor-made, actionable error message—e.g. *"To use tkinter, please run `dnf install python3-tkinter`"*—and possibly ending with automatic installation of the missing module.

The idea behind this PEP was discussed on the `python-dev mailing list`_.

.. _`python-dev mailing list`:
   https://mail.python.org/pipermail/python-dev/2016-July/145534.html


Backwards Compatibility
=======================

No problems with backwards compatibility are expected.  Distributions that are already patching Python modules to provide custom handling of missing dependencies can continue to do so unhindered.


Reference Implementation
========================

Reference implementation can be found on `GitHub`_ and is also accessible in the form of a `patch`_.

.. _`GitHub`: https://github.com/torsava/cpython/pull/1
.. _`patch`: https://github.com/torsava/cpython/pull/1.patch


References
==========

.. [#debian-patch] http://bazaar.launchpad.net/~doko/python/pkg3.5-debian/view/head:/patches/tkinter-import.diff


Copyright
=========

This document has been placed in the public domain.



..
   Local Variables:
   mode: indented-text
   indent-tabs-mode: nil
   sentence-end-double-space: t
   fill-column: 70
   coding: utf-8
   End:
