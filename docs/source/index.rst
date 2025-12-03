.. Bazar Kori documentation master file

Welcome to Bazar Kori's documentation!
======================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   modules

Bazar Kori - An E-commerce Platform
===================================

FastAPI-based marketplace with search, filter, and product management.

Modules
=======

.. autosummary::
   :toctree: _autosummary
   :recursive:

   main
   models.product
   controllers

API Endpoints
=============
- ``GET /api/search`` - Search products
- ``GET /api/filter`` - Advanced filtering
- ``GET /`` - Home page
- ``GET /filter`` - HTML filter page

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`