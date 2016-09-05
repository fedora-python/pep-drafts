PEP: XXX
Title: A Mechanism for Removing Stuff from the Standard Library
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


Specification
=============
.. The technical specification should describe the syntax and semantics of any new language feature. The specification should be detailed enough to allow competing, interoperable implementations for at least the current major Python platforms (CPython, Jython, IronPython, PyPy).


Rationale
=========
.. The rationale fleshes out the specification by describing what motivated the design and why particular design decisions were made. It should describe alternate designs that were considered and related work, e.g. how the feature is supported in other languages.
   The rationale should provide evidence of consensus within the community and discuss important objections or concerns raised during discussion.

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
