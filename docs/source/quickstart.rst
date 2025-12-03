Quick Start Guide
=================

Starting the Server
-------------------

.. code-block:: bash

   python main.py

Creating Your First Buyer Account
----------------------------------

1. Navigate to http://127.0.0.1:8002/buyer-signup
2. Fill in the registration form
3. Click "Sign Up"

Logging In as Buyer
-------------------

1. Go to http://127.0.0.1:8002/buyer-login
2. Enter your email and password
3. Click "Log In"

Admin Login
-----------

1. Go to http://127.0.0.1:8002/admin-login
2. Email: admin@bazar.com
3. Password: admin123

Available Routes
----------------

* GET / - Homepage
* GET /buyer-signup - Buyer registration
* POST /buyer-signup - Process registration
* GET /buyer-login - Buyer login
* POST /buyer-login - Process login
* GET /buyer-profile/{id} - View profile
* POST /update-profile/{id} - Update profile
* GET /admin-login - Admin login
* POST /admin-login - Process admin login
* GET /admin-dashboard - Admin dashboard