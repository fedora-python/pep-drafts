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
    to point to a formal-ish document.



Abstract
========

.. XXX:: Write this last :)


Rationale
=========

.. XXX::

    The perils of ``sudo pip``; need to install into ``/local``


Prior Art
=========

.. XXX::

    Debian's solution:
    downstream patch of distutils http://bazaar.launchpad.net/~ubuntu-branches/ubuntu/trusty/python2.7/trusty/view/head:/debian/patches/distutils-install-layout.diff#L281

    Install paths:
        - system-python: /usr/lib/dist_packages
        - distutils, (sudo pip): /usr/local/lib/dist_packages
        - pip: Permission Denied
        - python compiled from source (default): /usr/local/lib/site_packages

    Related disscussions:
        - https://mail.python.org/pipermail/distutils-sig/2016-January/028080.html
        - https://mail.python.org/pipermail/distutils-sig/2016-January/028087.html
        - http://bugs.python.org/issue27924
        - Relevant Fedora bug: https://bugzilla.redhat.com/show_bug.cgi?id=662034

Specification
=============

.. XXX::

    Where to install? What does the FHS say?

    Priority of ``/usr/lib`` vs. new location?

    What happens in virtualenvs?

    Making an isolated "System Python" ignore pip-installed packages?

    previous discussion: https://groups.google.com/forum/#!topic/pypa-dev/r6qsAmJl9t0

    FHS:
    The /usr/local hierarchy is for use by the system administrator when installing software locally. It needs to
    be safe from being overwritten when the system software is updated.

    If we consider pip as a tool for system administrators, we don't violate FHS using
    /usr/local/lib/pythonX.Y/site_packages as default install path.

    The reason why Debian uses /dist_packages:
    "The problem was this: if a sysadmin installed a from-source version of Python,
    say to do development or support some particular application environment, they
    would then install whatever libraries that application needed into
    /usr/local/lib/pythonX.Y/site-packages.  If /usr/local/.../site-packages was
    on the system Python's sys.path, then the act of building up your development
    environment could break system Python."

    **Solution 1:**
        Result of long discussion on pypa devel 2 years ago, similar to Debian's solution,
        more flexible (local_prefix).

        - Python options:
           - is_system_python
           - prefix
           - local_prefix

        - Python creates folders
           - prefix/.../dist-packages if is_system_python else site-packages
           - local_prefix/.../dist-packages if is_system_python else site-packages

        - Distutils installs to
           - local_prefix/.../dist-packages if is_system_python else site-packages

        - distutils --system installs to
           - prefix/.../dist-packages if is_system_python else site-packages

           - sudo pip installs to default distutils install location (local_prefix)

           - pip will never touch prefix folder while prefix != localprefix

        Advantages:
            - Specific location for each Python (system, built from source, ...)

        Disadvantages:
            - Necessary to change %{python3_sitelib|sitearch} macros
            - Too many changes
            - Too complicated


    **Solution 2:**
        - Python options:
           - prefix
           - local_prefix

        - Python creates folders
           - prefix/.../site-packages
           - local_prefix/.../site-packages

        - Distutils installs to
           - local_prefix/.../site-packages

        - distutils --system (flag for packaging purpose) installs to
           - prefix/.../site-packages

           - sudo pip installs to default distutils install location (local_prefix)

           - pip will never touch prefix folder while prefix != localprefix
             explicit system installation possible --root/--target

        Advantages:
            - System packages have their own location, separated from everything else
            - Similar to RubyGems's solution in Fedora
            - Changes in packaging macros not needed

        Disadvantages:
            - pip, distutils installed packages can collide with packages installed using Python from sources
            - --system flag wouldn't work for python where prefix == local_prefix


    **Solution 3:**
        Proposed by Donald Stufft on distutils-sig.
        Mixed installation path, mechanism to prevent collisions. Pip can determine
        that package is already installed by system, dnf and distutils cannot.

         - PEP 376 ignored by distutils
         - Necessary to switch to .dist-info metadata directory (setup.py install)
         - Implement logic to dnf, distutils to check if package isn't already installed
         - INSTALLER file could help to resolve updating and removing of packages



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
