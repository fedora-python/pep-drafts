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
    1. Don't forget 2 spaces after every sentence (Python developers should really read a manual of Style).
    2. Text should be longer than 70 but no longer than 79 characters.

Abstract
========

.. XXX::

    Write this last :)

    (~200 words)

    This PEP should handle step ``1)`` from the `initial discussion`_.

Motivation
==========
.. The motivation is critical for PEPs that want to change the Python language. It should clearly explain why the existing language specification is inadequate to address the problem that the PEP solves. PEP submissions without sufficient motivation may be rejected outright.

There are several use cases for including only a subset of Python's standard library. One is when a *stdlib* module with missing dependencies is skipped during the Python build process. Another is that a considerable amount of space can be saved by not distributing irrelevant parts of the standard library, such as ``TkInter`` on headless servers.

However, there is so far no formal specification of how to properly implement distribution of a subset of the standard library. Namely, how to safely handle attempts to import a missing *stdlib* module.


CPython
-------
When one of Python standard library modules (such as ``_sqlite3``) cannot be compiled during a Python build because of missing dependencies (e.g. SQLite header files), the module is simply skipped. If you then install this Python, and use it to try to import one of the missing modules, Python will go through the ``sys.path`` entries looking for it. It won't find it among the *stdlib* modules and thus it will continue onto ``site-packages`` and fail with an ``ImportError`` if it doesn't find it.

This introduces a possible security issue: ``site-packages`` can contain broken or even malicious code.


Linux distributions
-------------------
Many Linux distributions are already separating out parts of the standard library to standalone packages. Among the most commonly excluded modules are the ``TkInter`` module, since it draws in a dependency on the graphical environment, and the ``test`` module, as it only serves to test Python internally and is about as big as the rest of the standard library put together.

The methods of omission of these modules differ. For example, Debian patches the file ``Lib/tkinter/__init__.py`` to envelop the line ``import _tkinter`` in a *try-except* block and upon encountering an ``ImportError`` it simply adds the following to the error message: ``please install the python3-tk package`` [#debian-patch]_. Fedora and other distributions simply don't include the omitted modules and leave the rest as is.

Both these methods, nevertheless, introduce the aforementioned security issue of possibly importing missing *stdlib* modules from ``site-packages``.


Specification
=============
.. The technical specification should describe the syntax and semantics of any new language feature. The specification should be detailed enough to allow competing, interoperable implementations for at least the current major Python platforms (CPython, Jython, IronPython, PyPy).

When, for any reason, a standard library module is not to be included with the rest, a file with it's name and an extension ``.missing.py`` should be created and placed in the *stdlib* directory.

When Python tries to import a standard library module, it will look first for appropriately named files with the valid extensions (``.*.so``, ``.so``, ``.py``, ``.pyc``) and only if it still doesn't find the given module will it look for a file with the extension ``.missing.py`` and import it if found.

The file with the ``.missing.py`` extension can contain anything the distributor wishes, however, it *should* raise an ``ImportError``.


Rationale
=========
.. The rationale fleshes out the specification by describing what motivated the design and why particular design decisions were made. It should describe alternate designs that were considered and related work, e.g. how the feature is supported in other languages.
   The rationale should provide evidence of consensus within the community and discuss important objections or concerns raised during discussion.

Explanation of why we chose the specification: TBD.

.. XXX::

    Mention the needs of:
        * Linux distributions
            * (Debian is already doing this)

        * CPython (modules with missing dependencies may be skipped
          during build)

    (The MicroPython and AppInstaller use cases are not served by this
    particular PEP.)


Backwards Compatibility
=======================

.. XXX:: should not be a problem


Reference Implementation
========================

.. XXX:: link to patch (for ``importlib``?)


References
==========

.. [#debian-patch] http://bazaar.launchpad.net/~doko/python/pkg3.5-debian/view/head:/patches/tkinter-import.diff

..  TODO Where to reference this?
.. _initial discussion:
    https://mail.python.org/pipermail/python-dev/2016-July/145534.html


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
