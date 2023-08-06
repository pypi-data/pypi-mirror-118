==============
iSpin Data
==============

.. image:: https://travis-ci.org/lead-ratings/iSpin-data.svg?branch=master
    :target: https://gitlab.com/romowind_public/ispin_data


This package provides access to iSpin data for a specified turbine ID.  Its use is pretty straightforward::

    >>> import ispin_data.api as ispin
    
    >>> ispin.username = 'your_username'
    >>> ispin.password = 'your_password'
    
    >>> df = ispin.request_overview()
    # Returns iSpin installations
    
    >>> df = ispin.request_data(6)
    # Returns data for the installation with the turbine ID number 6. 
    # The start and end date can also be specified

    >>> t = ispin.request_turbine_type(6)
    # Returns the turbine type of the installation with the turbine ID number 6. 


Licenses
========

Nabla Wind Hub

ROMO Wind


Changelog
=========

0.1.0 (2021-08-24)
******************

* First release

0.3.0 (2021-08-30)
******************

* Second release

0.3.1 (2021-08-31)
******************

* Added author name and company to main code

* Third release

0.3.1 (2021-09-06)
******************

* Added a function to request the turbine type of an installation