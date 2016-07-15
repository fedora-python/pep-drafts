PEP: XXX
Title: A Mechanism for Removing Stuff from the Standard Library
Version: $Revision$
Last-Modified: $Date$
Author: Tomáš Orsava <torsava@redhat.com>,
        Petr Viktorin <pviktori@redhat.com>
Status: Draft
Type: Standards Track
Content-Type: text/x-rst
Created: 15-Jul-2016
Python-Version: 3.6
Post-History: 


Abstract
========

.. XXX::

    Write this last :)

    This PEP should handle step ``1)`` from the `initial discussion`_.


Rationale
=========

.. XXX::

    Mention the needs of:
        * Linux distributions
            * (Debian is already doing this)

        * CPython (modules with missing dependencies may be skipped
          during build)

    (The MicroPython and AppInstaller use cases are not served by this
    particular PEP.)


Prior Art
=========

.. XXX:: How does Debian do it?


Specification
=============

.. XXX::

    Add ``.py.missing`` "modules", with support in ``importlib``?

    How does Debian do this?


Backwards Compatibility
=======================

.. XXX:: should not be a problem


Reference Implementation
========================

.. XXX:: link to patch (for ``importlib``?)


References
==========

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
