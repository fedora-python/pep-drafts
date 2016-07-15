PEP: XXX
Title: Alternate location for System-Wide Installation on Linux
Version: $Revision$
Last-Modified: $Date$
Author: XXX
Status: Draft
Type: Standards Track
Content-Type: text/x-rst
Created: 15-Jul-2016
Python-Version: 3.6
Post-History: 

.. XXX::

    This might not end up as a PEP, since it's for pip, but it's still useful
    to write a formal-ish document.


Abstract
========

.. XXX:: Write this last :)


Rationale
=========

.. XXX::

    The perils of ``sudo pip``; need to install into ``/local``


Prior Art
=========

.. XXX:: How does Debian do it?


Specification
=============

.. XXX::

    Where to install? What does the FHS say?

    Priority of ``/usr/lib`` vs. new location?

    What happens in virtualenvs?

    Making an isolated "System Python" ignore pip-installed packages?


Backwards Compatibility
=======================

.. XXX:: should not be a problem, but check Debian


Reference Implementation
========================

.. XXX:: link to patch/PR


References
==========

.. XXX:: Add references here


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
